import numpy as np 
import math
from dataclasses import dataclass, field, replace 
from typing import Tuple, List, Optional, Callable  

import matplotlib.ticker as mticker 
import matplotlib.patches as mpatches 
import matplotlib.colors as mcolors 
import matplotlib.pyplot as plt 

from . import xaxis_options 
from ... import misc 
from ...data import phys_consts 
from ...data import isotopes 





def block_colorbar(pcolormesh, cbar, fig_fraction_cropped=0.3, fig = None, cutoff=None): 

    vmin, vmax = pcolormesh.get_clim() 

    img_arr = pcolormesh.get_array() 
    if cutoff is not None: 
        ind_include = np.where(img_arr>cutoff) 
        img_included = img_arr[ind_include] 
    else: 
        img_included = img_arr 
    img_min = np.nanmin(img_included) 
    img_max = np.nanmax(img_included)

    ax_colorbar = cbar.ax 
    cbar.outline.set_visible(False) 

    # Use background color of figure to block unused area of color bar 
    # Assumes original bg color was white and you applied a fig.patch.set_facecolor() and fig.patch.set_alpha() 
    # Blend that color with white to get what that color would be if it had an alpha of 1, 
    # so that applying it doesn't include a reduced alpha and become transparent, allowing the colorbar to be seen through it. 
    if fig is not None: 
        bg_color_unblended = np.array(fig.get_facecolor()) 
        bg_color = misc.blend_with_white(bg_color_unblended) 
    else: 
        bg_color = "white"

    # White rectangles to block unused area of color bar 
    bottom_left_block = mpatches.Rectangle(
        xy = (vmin, 0), 
        width = img_min-vmin, 
        height = fig_fraction_cropped, 
        color = bg_color, 
        lw = 0
    )
    ax_colorbar.add_patch(bottom_left_block)
    
    top_left_block = mpatches.Rectangle(
        xy = (vmin, 1), 
        width = img_min-vmin, 
        height = -fig_fraction_cropped, 
        color = bg_color, 
        lw = 0 
    )
    ax_colorbar.add_patch(top_left_block)

    bottom_right_block = mpatches.Rectangle(
        xy = (img_max, 0), 
        width = vmax-img_max, 
        height = fig_fraction_cropped, 
        color = bg_color, 
        lw = 0 
    )
    ax_colorbar.add_patch(bottom_right_block)
    
    top_right_block = mpatches.Rectangle(
        xy = (img_max, 1), 
        width = vmax-img_max, 
        height = -fig_fraction_cropped, 
        color = bg_color, 
        lw = 0 
    )
    ax_colorbar.add_patch(top_right_block)
    

    # Black border along remaining part of color bar 
    border_left = mpatches.Rectangle(
        xy = (vmin, fig_fraction_cropped), 
        width = img_min-vmin, 
        height = 1 - 2*fig_fraction_cropped, 
        color = "none", 
        lw = 1, 
        ec = "black", 
        clip_on = False) 
    ax_colorbar.add_patch(border_left) 

    border_y_pad = 0.0 
    border = mpatches.Rectangle(
        xy = (img_min, border_y_pad), 
        width = img_max-img_min, 
        height = 1-2*border_y_pad, 
        color = "none", 
        lw = 2, 
        ec = "black", 
        clip_on = False) 
    ax_colorbar.add_patch(border) 

    border_right = mpatches.Rectangle(
        xy = (img_max, fig_fraction_cropped), 
        width = vmax-img_max, 
        height = 1 - 2*fig_fraction_cropped, 
        color = "none", 
        lw = 1, 
        ec = "black", 
        clip_on = False) 
    ax_colorbar.add_patch(border_right) 





# Holds (x, y) coordinates of center and radius of a circle (typically in relative coordinates)
@dataclass
class Circle:
    x: float
    y: float
    r: float

    def as_tuple(self) -> Tuple[float,float,float]:
        return (self.x, self.y, self.r)





# Extra padding applied to a figure. Default = no padding. 
@dataclass
class Pad:
    left: float = 0.0 
    right: float = 0.0 
    bottom: float = 0.0 
    top: float = 0.0 

    def __mul__(self, other):
        if isinstance(other, (int, float)):
            return Pad(
                self.left   * other,
                self.right  * other,
                self.bottom * other,
                self.top    * other
            )
        return NotImplemented

    # allow scalar * Pad
    def __rmul__(self, other):
        return self.__mul__(other)

    def __truediv__(self, other):
        if isinstance(other, (int, float)):
            return Pad(
                self.left   / other,
                self.right  / other,
                self.bottom / other,
                self.top    / other
            )
        return NotImplemented





# Holds one "unit" of a plot: one big circle and one small circle. 
@dataclass
class PlotPositions:
    big: Circle
    small: Circle





# Holds radii used to generate a layout (relative sizes of big and small circles )
@dataclass 
class LayoutParams: 
    r_big: float = 1.0 
    r_small: float = 0.70 
    r_pad: float = 0.02 





# Calculate the circle that is tangent to two other circles 
def tangent_circles(
        c1: Circle, 
        c2: Circle, 
        r_new: float, 
        touch1: str = "external", 
        touch2: str = "external"
) -> List[Circle]: 

    def desired_distance(ri, touch):
        if touch == "external":
            return ri + r_new
        elif touch == "internal":
            return abs(ri - r_new)
        else:
            raise ValueError("touch must be 'external' or 'internal'")
    d1 = desired_distance(c1.r, touch1)
    d2 = desired_distance(c2.r, touch2)
    dx = c2.x - c1.x 
    dy = c2.y - c1.y
    D = math.hypot(dx, dy)
    if D == 0.0:
        raise ValueError("The two base circles are concentric (same center). Intersection is degenerate.")
    if D > (d1 + d2) + 1e-12 or D < abs(d1 - d2) - 1e-12:
        return []
    a = (d1*d1 - d2*d2 + D*D) / (2*D)
    h_sq = max(0.0, d1*d1 - a*a)
    h = math.sqrt(h_sq)
    xm = c1.x + a * (dx) / D
    ym = c1.y + a * (dy) / D
    rx = -dy * (h / D)
    ry =  dx * (h / D)

    c3a = Circle(
        x = xm + rx, 
        y = ym + ry, 
        r = r_new) 
    
    c3b = Circle(
        x = xm - rx, 
        y = ym - ry, 
        r = r_new) 
    
    if h <= 1e-12:
        return [(xm, ym)] # FIX: This should return a Circle object, but I don't even know what it does so I'll fix it if it breaks 
    else:
        return [c3a, c3b]






def calc_next_plot_positions(
        prev_plot_positions: PlotPositions, 
        parity: int, 
        layout_params: LayoutParams 
): 
    possible_big_circles = tangent_circles( 
        c1 = prev_plot_positions.big, 
        c2 = prev_plot_positions.small, 
        r_new = layout_params.r_big + layout_params.r_pad
    ) 

    next_big_circle = possible_big_circles[parity] 

    possible_small_circles = tangent_circles( 
        c1 = prev_plot_positions.big, 
        c2 = next_big_circle, 
        r_new = layout_params.r_small + layout_params.r_pad
    ) 

    next_small_circle = possible_small_circles[parity]

    next_plot_positions = PlotPositions( 
        big = next_big_circle, 
        small = next_small_circle
    )

    return next_plot_positions 





# Holds layout parameters and uses padding to create figure 
@dataclass
class Layout:
    """Holds circles in layout/data coordinates and performs conversions.""" 
    params: LayoutParams 
    positions: List[PlotPositions] = field(default_factory=list) 
    left: Optional[float] = None
    right: Optional[float] = None
    top: Optional[float] = None
    bottom: Optional[float] = None

    def add_initial(self, x_big, y_big, x_small, y_small):
        """seed with the first element (in layout coordinates).""" 
        plot_positions = PlotPositions( 
            big = Circle( 
                x = x_big, 
                y = y_big,
                r = self.params.r_big + self.params.r_pad,
            ), 
            small = Circle( 
                x = x_small,
                y = y_small,
                r = self.params.r_small + self.params.r_pad,
            )
        )
        self.positions.append(plot_positions)

        # initialize bounding box from the initial two circles
        self.left = min(
            x_big - self.params.r_big - self.params.r_pad, 
            x_small - self.params.r_small - self.params.r_pad)
        self.right = max(
            x_big + self.params.r_big + self.params.r_pad, 
            x_small + self.params.r_small + self.params.r_pad)
        self.bottom = min(
            y_big - self.params.r_big - self.params.r_pad, 
            y_small - self.params.r_small - self.params.r_pad)
        self.top = max(
            y_big + self.params.r_big + self.params.r_pad, 
            y_small + self.params.r_small + self.params.r_pad)

    def extend_positions(self, n_more: int):
        """Extend positions using your calc_next_plot_positions function, preserving your parity flipping.""" 
        prev_plot_positions = self.positions[-1] 
        for i in range(n_more): 
            parity = i%2 

            next_plot_positions = calc_next_plot_positions( 
                prev_plot_positions = prev_plot_positions, 
                parity = parity, 
                layout_params = self.params
            ) 

            prev_plot_positions = next_plot_positions 
            self.positions.append(next_plot_positions)

            self.left = min(
                self.left, 
                next_plot_positions.big.x - self.params.r_big - self.params.r_pad, 
                next_plot_positions.small.x - self.params.r_small - self.params.r_pad)
            self.right = max(
                self.right, 
                next_plot_positions.big.x + self.params.r_big + self.params.r_pad, 
                next_plot_positions.small.x + self.params.r_small + self.params.r_pad)
            self.bottom = min(
                self.bottom, 
                next_plot_positions.big.y - self.params.r_big - self.params.r_pad, 
                next_plot_positions.small.y - self.params.r_small - self.params.r_pad)
            self.top = max(
                self.top, 
                next_plot_positions.big.y + self.params.r_big + self.params.r_pad, 
                next_plot_positions.small.y + self.params.r_small + self.params.r_pad)

    def apply_padding(self, pad: Optional[Pad] = None):
        if pad is None:
            pad = Pad() # use default values (everything = 0)
        pad = pad * self.params.r_big 
        """Apply padding in layout units (same units as x/y/r). Common use: top_pad = factor * big_radius.""" 
        self.left  = (self.left  if self.left  is not None else 0.0) - pad.left
        self.right = (self.right if self.right is not None else 0.0) + pad.right
        self.bottom = (self.bottom if self.bottom is not None else 0.0) - pad.bottom
        self.top = (self.top if self.top is not None else 0.0) + pad.top

    def compute_width_height(self) -> Tuple[float,float]:
        if None in (self.left, self.right, self.top, self.bottom):
            raise RuntimeError("Bounding box not initialized.")
        width = self.right - self.left
        height = self.top - self.bottom
        return width, height

    def layout_to_fig_coords(self, x, y): #, width_data, height_data):
        """
        Convert (x,y) in layout coords to normalized figure coords [0..1] after final bbox
        width_data/height_data are the data-space width/height used to map to figure fractions.
        (We assume the figure is created with the finalized size computed by finalize_figsize.)
        """
        width, height = self.compute_width_height()
        x_norm = (x - self.left) / width
        y_norm = (y - self.bottom) / height
        return (x_norm, y_norm)

    def radius_to_fig_fraction(self, r_data, option=None):
        """
        Convert radius (data units) into a *figure-fraction diameter* after final bbox.
        The returned value is a fraction of the figure height (since we match total data-height -> figure height).
        diameter_fraction = (2*r_data) / (total_data_height)
        """
        width, height = self.compute_width_height()
        if option is None: 
            diameter_fraction = (2.0 * r_data) / np.min([width, height]) 
        if option == "width": 
            diameter_fraction = (2.0 * r_data) / width 
        if option == "height": 
            diameter_fraction = (2.0 * r_data) / height  
        return diameter_fraction

    def finalize_figsize(self, base_interior_height_in: float = 6.0):
        """
        Compute the figure size (in inches) required to preserve the interior visual scale
        when padding has been applied. This implements:
            fig_height_new = base_interior_height_in * (H_new / H_old)
        where H_old is the height before padding and H_new is after.
        So you must call this *after* computing initial bounding box but *before* applying padding,
        OR you can store the original pre-pad height externally and pass it here. To keep it simple:
        - Call compute_bounding_box() (initial)
        - Save H_old = top_old - bottom_old
        - call apply_padding(...)
        - then call finalize_figsize(base_interior_height_in, H_old)
        """
        raise NotImplementedError("Use finalize_figsize_with_prepad(H_old, base_interior_height_in) instead.")

    def finalize_figsize_with_prepad(self, H_old: float, base_interior_height_in: float = 6.0) -> Tuple[float, float]:
        """
        H_old: the original data-space height before padding
        base_interior_height_in: how many inches you want the interior (pre-pad) drawing to occupy
        Returns: (fig_width_in, fig_height_in)
        """
        width, height = self.compute_width_height()    # this is H_new based on current bbox (after padding)
        H_new = height
        if H_old <= 0:
            raise ValueError("H_old must be positive")
        # new figure height scaled so the interior mapping scale (data-unit -> inch) is preserved
        fig_height_new = base_interior_height_in * (H_new / H_old)
        fig_width_new = (width / height) * fig_height_new
        return fig_width_new, fig_height_new





def add_centered_axis(fig, center: Tuple[float,float], size_frac: float, projection=None, **kwargs):
    cx, cy = center
    w = float(size_frac)
    h = float(size_frac)
    left = cx - w/2
    bottom = cy - h/2
    return fig.add_axes([left, bottom, w, h], projection=projection, **kwargs)





@dataclass 
class CirclePlotConfig: 
    isotopes: list[isotopes.PlotItem] 
    title: str = "Error: title not provided to CirclePlotConfig"
    vmin: Optional[float] = None 
    vmax: Optional[float] = None
    cutoff: Optional[float] = 0.0
    major_ticks: Optional[list] = None 
    major_tick_labels: Optional[list] = None 
    major_tick_formatter: Optional[callable] = None 
    minor_ticks: Optional[list] = None 
    block_colorbar_cutoff: Optional[float] = None 





# Full circle plot for either composition or fusion 
def full_circle_plot( 
        profile, 
        history, 
        config: CirclePlotConfig, 
        xaxis: xaxis_options.ProfileXAxisOption = xaxis_options.PROFILEXAXIS_RADIUS, 
        base_interior_height_in: float = 4.0, 
        r_core_view_relative: float = 1.25, 
        pad: Optional[Pad] = Pad(left = 0.4, bottom = 0.8, top = 0.4, right=0.1), 
        layout_params: Optional[LayoutParams] = None): 



    # How big is the core? Determines how big the zoomed in plot needs to be 
    r_core = 0.0 
    for string in xaxis.core_strings: 
        radius = getattr(history, string)[profile.index] 
        if radius > r_core: 
            r_core = radius 
    
    # If there is no core, show a zoom-in on the center region 
    r_view_relative_default = 0.15 # relative to maximum radius 
    if r_core == 0.0: 
        r_core = np.max(xaxis.get_values(profile)) * r_view_relative_default 
    
    r_core_view = r_core_view_relative * r_core 
    do_small_plot = r_core_view < 0.025*np.max(xaxis.get_values(profile)) 

    

    # Only plot elements that reach a minimum threshold 
    relevant_isotopes = [] 
    for isotope in config.isotopes: 
        if np.max(isotope.evaluate_profile(profile)) > config.cutoff: 
            relevant_isotopes.append(isotope)
    
    # If none of the options meet the threshold, simply plot the first option 
    if len(relevant_isotopes) == 0: 
        relevant_isotopes.append(config.isotopes[0]) 

    # If only 1 plot shown, extend it horizontally so the title text fits 
    if len(relevant_isotopes) == 1: 
        new_pad = Pad(
            left = 1.0, 
            right = 1.0, 
            bottom = pad.bottom, 
            top = pad.top
        )
        pad = new_pad 
    


    # If no layout_params are provided, use default values 
    if layout_params is None: 
        layout_params = LayoutParams()
    


    # If only 1 plot is created, and it doesn't require the 2nd zoom-in subplot,  
    # set r_small=0 so there is not a gap between colorbar and big plot 
    # and reduce padding on left/right sides 
    if len(relevant_isotopes) == 1 and do_small_plot == False: 
        layout_params = LayoutParams(r_small=0)
        new_pad = Pad(
            left = 0.3, 
            right = 0.3, 
            bottom = pad.bottom, 
            top = pad.top
        ) 
        pad = new_pad 
    layout = Layout(params = layout_params)



    # initial seed (your values)
    x1_big, y1_big = 0.0, 0.0
    x1_small, y1_small = 0.0, 0.0 - layout.params.r_big - layout.params.r_small - 2*layout.params.r_pad
    layout.add_initial(x1_big, y1_big, x1_small, y1_small)

    # extend for the rest of the isotopes
    layout.extend_positions(len(relevant_isotopes)-1)
    width0, height0 = layout.compute_width_height()
    H_old = height0 
    print(width0, height0)


    layout.apply_padding(pad)  
    fig_w, fig_h = layout.finalize_figsize_with_prepad(H_old, base_interior_height_in=base_interior_height_in)
    fig = plt.figure(figsize=(fig_w, fig_h)) 
    print("FIGSIZE:", fig.get_size_inches())



    # Set the facecolor to very light gray 
    fig.patch.set_facecolor(misc.blend_with_white(input_color="black", alpha=0.05))

    # Title (gets replaced if in mode 1 or 2)
    fig.suptitle(
        config.title, 
        fontsize=18, 
        x=0.5, 
        y=0.97, 
        ha="center", 
        va="center"
    ) 

    # Subtitle 
    fig.text(
        0.5, 0.93, 
        f"{profile.initial_mass_string} $M_{{sun}}$ at {profile.age_string} old", 
        fontsize=12, ha='center')





    for ind, isotope in enumerate(relevant_isotopes):
        pos = layout.positions[ind] 

        # Big plot 
        big_center = layout.layout_to_fig_coords(pos.big.x, pos.big.y)
        big_size_frac = layout.radius_to_fig_fraction(layout.params.r_big)
        ax_big = add_centered_axis(
            fig = fig, 
            center = big_center, 
            size_frac = big_size_frac, 
            projection = 'polar'
        )
        big_mesh = ax_circle_plot(
            ax = ax_big, 
            profile = profile, 
            xaxis = xaxis, 
            f_r = isotope.evaluate_profile(profile), 
            cmap = isotope.evaluate_colormap(), 
            vmin = config.vmin, 
            vmax = config.vmax 
        ) 



        # Determine location of color bar (located beneath plots)
        x_small_fig, y_small_fig = layout.layout_to_fig_coords(pos.small.x, pos.small.y) 
        width_colorbar_fig = layout.radius_to_fig_fraction(layout.params.r_big, option="width") * 0.70 
        height_colorbar_fig = layout.radius_to_fig_fraction(layout.params.r_big, option="height") * 0.14   
        x_colorbar_fig = x_small_fig 
        y_colorbar_fig = layout.radius_to_fig_fraction(layout.params.r_big, option="height") * 0.3 
        left_colorbar_fig = x_colorbar_fig - width_colorbar_fig/2 
        bottom_colorbar_fig = y_colorbar_fig - height_colorbar_fig/2 

        # Add color bar as a new axis 
        ax_colorbar = fig.add_axes([left_colorbar_fig, bottom_colorbar_fig, width_colorbar_fig, height_colorbar_fig]) 
        cbar = plt.colorbar(
            mappable = big_mesh, 
            cax = ax_colorbar, 
            orientation = "horizontal") 
        cbar.set_label(f"{isotope.label}", fontsize=14) 

        # Major ticks: labeled with percentage, longer length tick 
        if config.major_ticks is not None: 
            ax_colorbar.xaxis.set_major_locator(mticker.FixedLocator(config.major_ticks))  
            ax_colorbar.xaxis.set_major_formatter(mticker.FixedFormatter(config.major_tick_labels)) 
        elif config.major_tick_formatter is not None: 
            ax_colorbar.xaxis.set_major_formatter(mticker.FuncFormatter(config.major_tick_formatter))
        ax_colorbar.tick_params(
            axis='x',
            which='major',
            length=10, 
            width=1.5,
            labelsize=12  # label fontsize
        )

        # Minor ticks: no labels, short tick  
        if config.minor_ticks is not None: 
            ax_colorbar.xaxis.set_minor_locator(mticker.FixedLocator(config.minor_ticks)) 
        ax_colorbar.tick_params(
            axis='x',
            which='minor',
            length=4,       
            width=1,
            labelsize=0  # no label
        )

        block_colorbar(
            pcolormesh = big_mesh, 
            cbar = cbar, 
            fig = fig, 
            cutoff = config.block_colorbar_cutoff)




        # Only add scale bars to first plot 
        if ind == 0: 

            # Big scale bar 
            x_big_scale = pos.big.x - (layout.params.r_big + 2*layout.params.r_pad) 
            y_big_scale = pos.big.y
            x_big_scale_fig, y_big_scale_fig = layout.layout_to_fig_coords(x_big_scale, y_big_scale)
            height_big_scale_fig = layout.radius_to_fig_fraction(layout.params.r_big/2, option="height") 
            width_big_scale_fig = 0 
            ax_big_scale = fig.add_axes([x_big_scale_fig, y_big_scale_fig, width_big_scale_fig, height_big_scale_fig])
            ax_big_scale.set_xticks([])
            ax_big_scale.set_yticks([0.0, 0.5, 1.0])

            ax_big_scale.set_yticklabels(
                [
                    f"{misc.round_sigfigs(np.max(xaxis.get_values(profile)), 2)} "
                    f"{xaxis.xlabel}"
                    if tick == 0.5 else ""
                    for tick in ax_big_scale.get_yticks()
                ],
                va="center",
                fontsize=14, 
                rotation=90 
            )



        # If core is large enough, we don't need the zoomed in plot to see it, so skip the small axis  
        if do_small_plot == False:  
            continue 

        # Small plot 
        small_center = layout.layout_to_fig_coords(pos.small.x, pos.small.y)
        small_size_frac = layout.radius_to_fig_fraction(layout.params.r_small)
        ax_small = add_centered_axis(
            fig = fig, 
            center = small_center, 
            size_frac = small_size_frac, 
            projection = 'polar', 
            zorder = 10 # Make sure small axis appears above connecting lines 
        )
        ax_circle_plot(
            ax = ax_small, 
            profile = profile, 
            xaxis = xaxis, 
            f_r = isotope.evaluate_profile(profile), 
            cmap = isotope.evaluate_colormap(), 
            vmin = config.vmin, 
            vmax = config.vmax, 
            r_max = r_core_view
        )



        # Show where on the big plot the zoomed in plot is located 
        theta = np.linspace(0, 2*np.pi, 36)
        ax_big.plot(theta, np.repeat(r_core_view, len(theta)), color="black", linestyle=(0, (5, 5)), lw=0.6) 

        # Add lines connecting small plot to location of small plot within big plot 
        for side in (1,2): # Repeat for left and right sides of plot 
        
            # Calculate position of side of small plot, in figure coordinates 
            x_side_small_fig, y_side_small_fig = layout.layout_to_fig_coords(
                pos.small.x + (-1)**side * layout.params.r_small, 
                pos.small.y)

            # Calculate position of side of core shown in the big plot... converted to figure coordinates 
            x_side_big_fig, y_side_big_fig = layout.layout_to_fig_coords(
                pos.big.x + (-1)**side * layout.params.r_big * r_core_view/np.max(xaxis.get_values(profile)), 
                pos.big.y)

            # Draw a line between them 
            line = plt.Line2D(
                [x_side_big_fig, x_side_small_fig],   
                [y_side_big_fig, y_side_small_fig],   
                transform = fig.transFigure,
                color = "black",
                linestyle = (0, (5, 5)), 
                lw = 0.8,
            )
            fig.lines.append(line)

        # Replace small axis border with dashed lines 
        for spine in ax_small.spines.values():
            spine.set_linestyle((0, (5, 5))) 
            spine.set_color("black") 
            spine.set_linewidth(1)



        if ind == 0: 
            # Small scale bar 
            x_small_scale = pos.small.x - (layout.params.r_small + 2*layout.params.r_pad) 
            y_small_scale = pos.small.y
            x_small_scale_fig, y_small_scale_fig = layout.layout_to_fig_coords(x_small_scale, y_small_scale)
            height_small_scale_fig = layout.radius_to_fig_fraction(layout.params.r_small/2, option="height") 
            width_small_scale_fig = 0 
            ax_small_scale = fig.add_axes([x_small_scale_fig, y_small_scale_fig, width_small_scale_fig, height_small_scale_fig])
            ax_small_scale.set_xticks([])
            ax_small_scale.set_yticks([0.0, 0.5, 1.0])

            ax_small_scale.set_yticklabels(
                [
                    f"{misc.round_sigfigs(r_core_view, 2)} "
                    f"{xaxis.xlabel}"
                    if tick == 0.5 else ""
                    for tick in ax_small_scale.get_yticks()
                ],
                va="center",
                fontsize=12, 
                rotation=90
            )



    return fig 






def ax_circle_plot(ax, profile, f_r, xaxis=xaxis_options.PROFILEXAXIS_RADIUS, cmap=None, vmin=None, vmax=None, r_max=None):
    """
    Plot a circular radial intensity pattern using a polar projection.
    
    Parameters:
        r               : array-like, radial coordinates (either mass coordinate or radius) 
        f_r             : array-like, intensity values corresponding to r (i.e., f(r))
        cmap            : str, colormap name
        vmin, vmax      : color normalization limits (optional)
    """

    r = xaxis.get_values(profile)

    # Add extra points near zero so it doesn't look like there's a hole at the center of the star 
    for _ in range(100): 
        f_r = np.append(f_r, f_r[np.argmin(r)])
        r = np.append(r, np.min(r)/2) 

    # Polar plot 
    theta = np.linspace(0, 2 * np.pi, 360)
    R, THETA = np.meshgrid(r, theta)
    H = np.tile(f_r, (len(theta), 1))
    mesh = ax.pcolormesh(THETA, R, H, cmap=cmap, shading='auto', vmin=vmin, vmax=vmax)

    # R limit 
    if r_max is not None: 
        ax.set_ylim(0, r_max)

    ax.set_xticks([])
    ax.set_yticks([])

    return mesh









def circle_composition(profile, history, xaxis: xaxis_options.ProfileXAxisOption = xaxis_options.PROFILEXAXIS_RADIUS): 

    config = CirclePlotConfig( 
        isotopes = isotopes.ISOTOPES, 
        title = "Interior composition", 
        cutoff = 0.1, 
        vmin = 0, 
        vmax = 1, 
        major_ticks = [0.2, 0.5, 0.8], 
        major_tick_labels = ["20%", "50%", "80%"], 
        minor_ticks = [i/10 for i in range(11)]
    )

    fig = full_circle_plot(  
        profile = profile, 
        history = history, 
        xaxis = xaxis, 
        config = config, 
    )  
    return fig 





# WORK IN PROGRESS 
# def circle_composition_log(profile, history, xaxis: xaxis_options.ProfileXAxisOption = xaxis_options.PROFILEXAXIS_RADIUS): 

#     new_isotopes = [
#         isotopes.PlotItem(
#             profile_key=i.profile_key,
#             profile_compute=lambda p: np.log10(p.log_D_ovr)
#             history_key=i.history_key,
#             label=i.label,
#             color=i.color,
#             cmap=i.cmap,
#             show_initial_abundance=i.show_initial_abundance
#         )
#         for i in isotopes.CONVECTIONS
#     ]
    
#     config = CirclePlotConfig( 
#         isotopes = isotopes.ISOTOPES, 
#         title = "Interior composition", 
#         cutoff = -6, 
#         vmin = -6, 
#         vmax = 0, 
#         # major_ticks = [0.2, 0.5, 0.8], 
#         # major_tick_labels = ["20%", "50%", "80%"], 
#         # minor_ticks = [i/10 for i in range(11)]
#     )

#     fig = full_circle_plot(  
#         profile = profile, 
#         history = history, 
#         xaxis = xaxis, 
#         config = config, 
#     )  
#     return fig 






def circle_fusion(profile, history, xaxis: xaxis_options.ProfileXAxisOption = xaxis_options.PROFILEXAXIS_RADIUS): 

    specific_L = np.max(profile.luminosity)*phys_consts.L_sun / (profile.initial_mass*phys_consts.M_sun) 
    max_fusion = np.max(profile.eps_nuc) 
    if max_fusion>specific_L: 
        vmax = max_fusion 
    else: 
        vmax = specific_L*10

    config = CirclePlotConfig( 
        isotopes = isotopes.FUSION_RATES, 
        title = "Fusion rate inside star", 
        cutoff = vmax/100, 
        vmin = 0, 
        vmax = vmax 
    )

    fig = full_circle_plot(  
        profile = profile, 
        history = history, 
        xaxis = xaxis, 
        config = config, 
        r_core_view_relative=1.5
    )  
    return fig 






def circle_convection(profile, history, xaxis: xaxis_options.ProfileXAxisOption = xaxis_options.PROFILEXAXIS_RADIUS): 

    vmax = np.max([np.max(x.evaluate_profile(profile)) for x in isotopes.CONVECTIONS]) 

    config = CirclePlotConfig( 
        isotopes = isotopes.CONVECTIONS, 
        title = "Convective regions inside star", 
        cutoff = vmax/100, 
        vmax = vmax, 
    )

    fig = full_circle_plot(  
        profile = profile, 
        history = history, 
        xaxis = xaxis, 
        config = config, 
    ) 
    return fig 





def circle_convection_log(profile, history, xaxis: xaxis_options.ProfileXAxisOption = xaxis_options.PROFILEXAXIS_RADIUS): 

    new_isotopes = [
        isotopes.PlotItem(
            profile_key=i.profile_key,
            profile_compute=None,   # Overridden
            history_key=i.history_key,
            label=i.label,
            color=i.color,
            cmap=i.cmap,
            show_initial_abundance=i.show_initial_abundance
        )
        for i in isotopes.CONVECTIONS
    ]

    def find_max_and_min(x, cutoff): 
        ind_include = np.where(x>cutoff)[0] # Minimum value, if we exclude 1e-99 which is practically zero 
        if len(ind_include) == 0: 
            min_val = np.nan 
        else: 
            min_val = np.min(x[ind_include]) 
        max_val = np.max(x) 
        return (min_val, max_val) 
    
    # Find range that convection levels vary across, ignoring any curves that stay at 1e-99 the whole time 
    min_arr = [] 
    max_arr = [] 
    cutoff = -70 # remember, these numbers are all log base 10. 
    for iso in new_isotopes:
        (min_val, max_val) = find_max_and_min(iso.evaluate_profile(profile), cutoff) 
        min_arr.append(min_val)
        max_arr.append(max_val) 
    
    vmin = np.nanmin(min_arr)
    vmax = np.nanmax(max_arr)

    locator = mticker.MaxNLocator(nbins=3) 
    ticks = locator.tick_values(vmin, vmax)
    labels = [f"$10^{{{x}}}$" for x in ticks]

    config = CirclePlotConfig( 
        isotopes = new_isotopes, 
        title = "Convective regions inside star", 
        cutoff = cutoff, 
        vmin = vmin, 
        vmax = vmax, 
        block_colorbar_cutoff = cutoff, 
        major_ticks = ticks, 
        major_tick_labels = labels 
    )

    fig = full_circle_plot(  
        profile = profile, 
        history = history, 
        xaxis = xaxis, 
        config = config, 
    ) 
    return fig 






def circle_temp(profile, history, xaxis: xaxis_options.ProfileXAxisOption = xaxis_options.PROFILEXAXIS_RADIUS): 


    config = CirclePlotConfig( 
        isotopes = [isotopes.PlotItem(
            profile_compute = lambda p: 10**p.logT, 
            label = "Temperature (K)", 
            cmap = "plasma"
        )], 
        title = "Temperature", 
        major_tick_formatter=mticker.EngFormatter()
    )

    fig = full_circle_plot(  
        profile = profile, 
        history = history, 
        xaxis = xaxis, 
        config = config, 
    ) 
    return fig 

