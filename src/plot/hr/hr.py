import matplotlib.pyplot as plt 
import matplotlib.ticker as mticker 
import matplotlib.transforms as mtransforms 
import matplotlib.patches as mpatches 
import itertools 
import functools 
import numpy as np 
import labellines 
import scipy 

from . import locators 
from . import spectral_types 
from ...data import phys_consts 
from ... import misc 





class HRDiagram:

    def __init__(
        self,
        hide_paths=False,
        hide_grid=True,
        hide_legend=True, 
        hide_ticks=True
    ):
        # Store feature flags
        self.hide_paths = hide_paths
        self.hide_grid = hide_grid
        self.hide_legend = hide_legend
        self.hide_ticks = hide_ticks 

        # Setup base figure and axes
        self.fig, self.ax = plt.subplots(figsize=(12.8, 7))
        self.fig.subplots_adjust(top=0.82, bottom=0.13, left=0.10, right=0.81)

        # X axis: Temperature
        self.ax.set_xlabel("Surface temperature (K)", fontsize=18, labelpad=14)
        self.ax.set_xscale("log")
        self.ax.set_xlim((20_000, 3000)) 

        # Y axis: Luminosity
        self.ax.set_ylabel("Luminosity ($L_{{sun}}$)", fontsize=18, labelpad=14)
        self.ax.set_yscale("log")
        self.ax.set_ylim((1e-6, 1e8))

        # Grid, ticks, title
        self.setup_ticks() 
        self.ax.tick_params(labelsize=14, length=10, which="major")
        self.grid(alpha=0.5, which="both")
        self.ax.set_title("Evolutionary Path Across HR Diagram", fontsize=20, pad=50)

        # Setup events
        self.lines = []
        self._legend = None
        self._connect_pan_events() 
        # self._connect_home_events() 





    def add_path(self, history, color=None, label=None, lw=2, alpha=1, modelnum_start=None, modelnum_end=None):
        """Add an evolutionary track to the HR diagram."""
        ind_start = 0 if modelnum_start is None else modelnum_start - 1
        ind_end = -1 if modelnum_end is None else modelnum_end - 1 + 1 # Add one to ending to remove gaps between segments 

        line, = self.ax.plot(
            10**history.log_Teff[ind_start:ind_end],
            10**history.log_L[ind_start:ind_end],
            color=color,
            label=label,
            lw=lw,
            alpha=alpha
        )
        self.lines.append(line)





    def grid(self, **kwargs):
        """Enable grid with initial settings."""
        self.ax.grid(True, **kwargs)





    def legend(self, **kwargs):
        """Create a legend and optionally connect it to hide during panning."""
        self._legend = self.ax.legend(**kwargs)





    def setup_ticks(self): 

        # X axis 
        self.ax.xaxis.set_major_locator(locators.MajorLogLocator()) 
        self.ax.xaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"{int(x):,}")) 
        self.ax.xaxis.set_minor_locator(locators.MinorLogLocator()) 
        self.ax.xaxis.set_minor_formatter(mticker.NullFormatter())  
        
        # Y axis 
        self.ax.yaxis.set_major_locator(mticker.LogLocator(numticks=5))
        self.ax.yaxis.set_minor_locator(mticker.LogLocator(subs='auto', numticks=2))





    def add_radius_contours(self): 

        lines = [] 
        temp_range = np.logspace(2, 6, 100)
        for radius in np.logspace(-6, 6, 7):
            
            # Calculate Luminosity using L = 4pi*sigma * R^2 * T^4
            L_range = (
                4*np.pi * phys_consts.sigma_sb *
                (radius*phys_consts.R_sun)**2 *
                (temp_range)**4 
            ) / phys_consts.L_sun 

            # Add line to list 
            line = self.ax.plot(temp_range, L_range, label=f"{radius:,g} $R_{{sun}}$", color='#b0b0b0', alpha=0.8, lw=0.8)
            lines.append(line[0])

        # Add the labels twice: Once to the left side of the plot, and once to the right side  
        xleft = np.log10(self.ax.get_xlim()[1])
        xright = np.log10(self.ax.get_xlim()[0])
        xdiff = xright - xleft
        xleft_label = xleft + xdiff*0.05 
        xright_label = xright - xdiff*0.05
        _ = labellines.labelLines(lines, xvals=10**xleft_label, alpha=0.5, color="black") 
        _ = labellines.labelLines(lines, xvals=10**xright_label, alpha=0.5, color="black") 

        # After adding contour labels, remove the labels from each line object so that it doesn't appear in the legend 
        for line in lines: 
            line.set_label(None)




    def _connect_pan_events(self):
        """Central event manager for hiding features during pan and zoom."""



        def check_if_valid_event(event, check_for_inaxes): 
            """Make sure the button press is actually a pan/zoom"""
            if event.button not in (1, 3): 
                return False 
            if check_for_inaxes: 
                if event.inaxes != self.ax:
                    return False
            toolbar = getattr(event.canvas, "toolbar", None)
            if toolbar == False: 
                return False 
            if toolbar.mode not in ("pan/zoom", "zoom rect"): 
                return False 
            else: 
                return True 



        def on_press(event):

            # Escape if button press not valid 
            if check_if_valid_event(event, check_for_inaxes=True) == False: 
                return 
            
            # Hide evolutionary tracks 
            if self.hide_paths:
                for line in self.lines:
                    line.set_visible(False)

            # Hide grid during pan
            if self.hide_grid:
                self.ax.grid(False, which='major')
                self.ax.grid(False, which='minor')

            # Hide legend during pan
            if self.hide_legend and self._legend is not None:
                self._legend.set_visible(False)

            # Hide ticks labels during pan
            if self.hide_ticks:

                # X axis 
                self.ax.xaxis.set_major_locator(mticker.NullLocator()) 
                self.ax.xaxis.set_major_formatter(mticker.NullFormatter()) 
                self.ax.xaxis.set_minor_locator(mticker.NullLocator()) 
                self.ax.xaxis.set_minor_formatter(mticker.NullFormatter())  

                # Y axis 
                self.ax.yaxis.set_major_locator(mticker.NullLocator()) 
                self.ax.yaxis.set_minor_locator(mticker.NullLocator()) 
            
            # Hide spectral labels and spans
            self._set_spectral_label_visibility(False) 
            if self.hide_spectraltype_spans: 
                self._set_spectral_spans_visibility(False)
            
            self.fig.canvas.draw_idle()



        def on_release(event):

            # Escape if button press not valid 
            if check_if_valid_event(event, check_for_inaxes=False) == False: 
                return 
            
            # Restore evolutionary tracks 
            if self.hide_paths:
                for line in self.lines:
                    line.set_visible(True)

            # Restore grid
            if self.hide_grid:
                self.ax.grid(True, which='major')
                self.ax.grid(True, which='minor')

            # Restore legend
            if self.hide_legend and self._legend is not None:
                self._legend.set_visible(True)

            # Restore minor ticks
            if self.hide_ticks:
                self.setup_ticks() 

            # Restore visibility and recalculate labels
            self._draw_spectral_labels()  
            if self.hide_spectraltype_spans: 
                self._set_spectral_spans_visibility(True)
                
            self.fig.canvas.draw_idle()



        self.fig.canvas.mpl_connect('button_press_event', on_press)
        self.fig.canvas.mpl_connect('button_release_event', on_release)





    def add_spectral_type_labels(self, min_spacing_pixels=120, hide_spectraltype_spans=True):
        """
        Add spectral type labels (OBAFGKM sequence) and shaded spectral bands.
        Labels automatically hide during pan/zoom and reappear afterward.
        """

        # Store settings and initialize storage
        self.hide_spectraltype_spans = hide_spectraltype_spans
        self._min_spacing_pixels = min_spacing_pixels
        self._spectral_label_elements = []   # list of (text, line) pairs
        self._spectral_spans = []
        self._spectral_color_cycle = itertools.cycle(["black", "white"])

        # Add label to right side of spectral types
        self.fig.text(0.84, 0.85, "\u2190 Spectral type", fontsize=12)


        # --- Helper: Determine which subtypes fit in current view ---
        def _sample_visible_subtypes():
            xmax, xmin = self.ax.get_xlim()
            selected = []
            spectral_letters = "OBAFGKM"

            for stype in spectral_types.SPECTRAL_TYPES:
                if stype.letter not in spectral_letters:
                    continue 
                for subtype in stype.subtypes: 
                    if xmin <= subtype.temp <= xmax:
                        x_disp = self.ax.transData.transform((subtype.temp, 0))[0] 
                        if not selected or abs(x_disp - selected[-1][1]) >= min_spacing_pixels:
                            selected.append((subtype, x_disp))
            return [subtype for subtype, _ in selected]



        # --- Helper: Draw or refresh labels ---
        def _draw_labels():
            # Remove old labels
            for txt, line in getattr(self, "_spectral_label_elements", []):
                txt.remove()
                line.remove()
            self._spectral_label_elements = []

            subtypes_to_display = _sample_visible_subtypes()
            transform = self.ax.get_xaxis_transform(which='grid')

            for subtype in subtypes_to_display:
                x = subtype.temp

                # Connector line (like a tick)
                connector = self.ax.plot(
                    [x, x], [1.0, 1.015],
                    transform=transform, color='black', lw=1.0, clip_on=False
                )[0]

                # Text label
                txt = self.ax.text(
                    x, 1.02,
                    f"{subtype.label.replace('V', '')} \n({int(subtype.temp):,} K)",
                    transform=transform,
                    ha='center', va='bottom',
                    fontsize=10, color='black'
                )

                self._spectral_label_elements.append((txt, connector))

            self.fig.canvas.draw_idle()



        # Colored regions above plot corresponding to each spectral type 
        if not hasattr(self, "_spectral_spans") or not self._spectral_spans:
            for st in spectral_types.SPECTRAL_TYPES:

                trans = mtransforms.blended_transform_factory(self.ax.transData, self.ax.transAxes)
                xmin = st.temp_range[1] 
                xmax = st.temp_range[0]
                color = st.color 

                # # Highlight inside plot 
                # self.ax.axvspan(
                #     xmin, xmax, 
                #     facecolor = color, 
                #     alpha = 0.2) 
                
                # # Add borders between regions 
                # self.ax.axvline(xmin, color=color, lw=0.8, zorder=0)
                
                # Add colored rectangle above plot
                span = mpatches.Rectangle(
                    xy = (xmin, 1.00), 
                    width = xmax-xmin, 
                    height = 0.1, 
                    transform = trans, 
                    facecolor = color, 
                    alpha = 1.0, 
                    edgecolor = "white", 
                    linewidth = 2, 
                    clip_on = True ) 
                self.ax.add_patch(span) 

                # Set clip boundary of rectangle 
                clip_fig_rect = mpatches.Rectangle( 
                    xy = (self.fig.subplotpars.left, 0), 
                    width = self.fig.subplotpars.right - self.fig.subplotpars.left, 
                    height = 1.0, 
                    transform=self.fig.transFigure, 
                    facecolor="none", 
                    edgecolor="none")
                span.set_clip_path(clip_fig_rect) 

                self._spectral_spans.append(span)

        # Store helper functions for later re-use
        self._draw_spectral_labels = _draw_labels
        self._sample_visible_subtypes = _sample_visible_subtypes

        # Initial draw
        _draw_labels()





    def _set_spectral_label_visibility(self, visible):
        """Show or hide both text and connector lines."""
        if not hasattr(self, "_spectral_label_elements"):
            return
        for txt, connector in self._spectral_label_elements:
            txt.set_visible(visible)
            connector.set_visible(visible)





    def _set_spectral_spans_visibility(self, visible):
        """Show or hide the background spectral spans."""
        if not hasattr(self, "_spectral_spans"):
            return
        for span in self._spectral_spans:
            span.set_visible(visible)





    def _connect_home_events(self): 

        def _refresh_spectral_labels(event=None):
            if hasattr(self, "_draw_spectral_labels"):
                self._draw_spectral_labels()
                self.fig.canvas.draw_idle()



        # Ensure the toolbar is initialized
        manager = plt.get_current_fig_manager()
        toolbar = manager.toolbar

        # For Qt-based backends, toolbar has .actions() that list all buttons
        for action in toolbar.actions(): 
            if action.text().lower() in ["home", "back", "forward"]:
                action.triggered.connect(_refresh_spectral_labels)
            




    # Add model labels to points on an HR diagram, skipping some models to avoid overlapping labels 
    def add_modelnum_labels(self, history, modelnum_now=None):
        ax = self.ax


        # Check if too points are too close (the labels will overlap)
        def calc_is_too_close(point1, point2, current_bounds): 

            min_x_fractional_sep = 0.08  
            min_y_fractional_sep = 0.08  

            xlim, ylim = current_bounds 

            x_sep = np.abs(point1[0]-point2[0]) 
            y_sep = np.abs(point1[1]-point2[1]) 
            
            log_xlim = np.log10(xlim) 
            log_ylim = np.log10(ylim)

            log_xrange = max(log_xlim) - min(log_xlim) 
            log_yrange = max(log_ylim) - min(log_ylim) 

            # Check whether the two points are too close 
            if x_sep < min_x_fractional_sep*log_xrange and y_sep < min_y_fractional_sep*log_yrange:
                return True
            else: 
                return False  



        # Function that runs every time axis limits are changed 
        def update_secondary_axis(ax): 

            # 1) Remove previous points, so only current ones are shown on plot 

            if hasattr(ax, "_model_points"):
                ax._model_points.remove() 
            if hasattr(ax, "_model_label_points"):
                ax._model_label_points.remove() 
            if hasattr(ax, "_model_labels"):
                for label in ax._model_labels: 
                    label.remove()  
            if hasattr(ax, "_modelnum_now_point"): 
                ax._modelnum_now_point.remove() 
            if hasattr(ax, "_modelnum_now_label"): 
                ax._modelnum_now_label.remove() 
            


            # 2) Calculate positions where models are available 

            # Get current axes bounds 
            xlim = ax.get_xlim() 
            ylim = ax.get_ylim() 

            # Return x,y coords of points within axes bounds 
            ind_models_available = history.model_numbers_available-1 
            log_Teff = history.log_Teff[ind_models_available]
            log_L = history.log_L[ind_models_available]
            ind_in_view = functools.reduce(
                np.intersect1d, 
                [
                    np.where(10**log_Teff>min(xlim)), 
                    np.where(10**log_Teff<max(xlim)), 
                    np.where(10**log_L>min(ylim)), 
                    np.where(10**log_L<max(ylim)) ] )
            log_Teff_in_view = log_Teff[ind_in_view]
            log_L_in_view = log_L[ind_in_view]

            if len(log_Teff_in_view) == 0:
                ax._model_points = ax.scatter([], []) 
                ax._model_label_points = ax.scatter([], []) 
                ax._model_labels = [] 
                ax._modelnum_now_point = ax.scatter([], []) 
                ax._modelnum_now_label = ax.text([], [], "") 
                ax.figure.canvas.draw_idle()
                return


            # 3) Calculate positions to place labels (subset of points with model numbers, so that labels don't overlap)

            log_Teff_labeled = [log_Teff_in_view[0]]
            log_L_labeled = [log_L_in_view[0]]

            # try to use modelnum_now if it’s valid and in range
            if modelnum_now is not None:
                x = history.log_Teff[modelnum_now - 1]
                y = history.log_L[modelnum_now - 1] 

                in_x_range = np.log10(min(xlim)) < x < np.log10(max(xlim))
                in_y_range = np.log10(min(ylim)) < y < np.log10(max(ylim))

                if in_x_range and in_y_range:
                    log_Teff_labeled = [x]
                    log_L_labeled = [y] 

            # Loop over all available points 
            for i in np.arange(1, len(log_Teff_in_view)): 

                x = log_Teff_in_view[i] 
                y = log_L_in_view[i] 

                # Check if the current point should be labeled or not 
                # Only label if this point isn't too close to any of the other labels 
                is_too_close = False 
                for j in range(len(log_Teff_labeled)): 
                    x0 = log_Teff_labeled[j]
                    y0 = log_L_labeled[j] 
                    if calc_is_too_close((x,y), ((x0,y0)), (xlim,ylim)): 
                        is_too_close = True 
                        break 
                if is_too_close: 
                    continue 
            
                # If we haven't skipped to the next point, the current point is not too close to any of the current labels, so add it to the list 
                log_Teff_labeled.append(x)
                log_L_labeled.append(y) 

            # Convert lists back to numpy array 
            log_Teff_labeled = np.array(log_Teff_labeled) 
            log_L_labeled = np.array(log_L_labeled) 

            # Remove current model number from labels list and apply a separate label to it 
            if modelnum_now is not None: 
                log_Teff_labeled = log_Teff_labeled[log_Teff_labeled != history.log_Teff[modelnum_now-1]] 
                log_L_labeled = log_L_labeled[log_L_labeled != history.log_L[modelnum_now-1]] 
            


            # 4) Add labels and points calculated in previous sections to the plot 
            
            # Add points to all positions with models 
            ax._model_points = ax.scatter(
                10**log_Teff_in_view, 10**log_L_in_view, 
                zorder=10, color="white", ec="black", s=5) 

            # Add points to the subset of positions with labels 
            ax._model_label_points = ax.scatter(
                10**log_Teff_labeled, 10**log_L_labeled, 
                zorder=30, color="white", edgecolor="black", s=20) 

            # The labels themselves 
            ax._model_labels = [] 
            for i in range(len(log_Teff_labeled)): 
                ax._model_labels.append( ax.text(
                    10**log_Teff_labeled[i], 
                    10**log_L_labeled[i], 
                    np.where(history.log_Teff == log_Teff_labeled[i])[0][0]+1,  
                    fontsize=10, ha='left', va='bottom', zorder=20, clip_on=True, 
                    bbox=dict(facecolor='white', edgecolor='black', alpha=1.0, boxstyle='round,pad=0.2')) )

            if modelnum_now is not None: 
                
                # Point for the currently selected model 
                ax._modelnum_now_point = ax.scatter(
                    10**history.log_Teff[modelnum_now-1], 10**history.log_L[modelnum_now-1], 
                    zorder=30, color="gold", edgecolor="black", s=20) 
            
                # Label the currently selected model 
                ax._modelnum_now_label = ax.text(
                    10**history.log_Teff[modelnum_now-1], 10**history.log_L[modelnum_now-1], 
                    modelnum_now,  
                    fontsize=12, ha='left', va='bottom', zorder=20, clip_on=True, 
                    bbox=dict(facecolor='gold', edgecolor='black', alpha=1.0, boxstyle='round,pad=0.2')) 



        # 5) Connect function to axis so it automatically updates on limit changes 

            # Idk what this does 
            ax.figure.canvas.draw_idle()
            
        # Re-run this function every time the x or y axes limits change 
        ax.callbacks.connect('xlim_changed', update_secondary_axis)
        ax.callbacks.connect('ylim_changed', update_secondary_axis)
        update_secondary_axis(ax)





    def add_age_labels(self, history): 

        # Find ages to place labels 
        log_L_interp = scipy.interpolate.interp1d(history.star_age, history.log_L, bounds_error=False, fill_value=np.nan) 
        log_T_interp = scipy.interpolate.interp1d(history.star_age, history.log_Teff, bounds_error=False, fill_value=np.nan) 
        locator = mticker.MaxNLocator(
            nbins=100, 
            steps=[1, 2, 5], 
        )
        ages = locator.tick_values(0, np.max(history.star_age)) 
        logx = log_T_interp(ages)
        logy = log_L_interp(ages)

        # Calculate text to display at each label 
        labels = [f"{misc.to_engineering(age)}yr" for age in ages] 


        # Check if too points are too close (the labels will overlap)
        def calc_is_too_close(point1, point2, current_bounds): 

            min_x_fractional_sep = 0.07 
            min_y_fractional_sep = 0.07    

            xlim, ylim = current_bounds 

            x_sep = np.abs(point1[0]-point2[0]) 
            y_sep = np.abs(point1[1]-point2[1]) 
            
            log_xlim = np.log10(xlim) 
            log_ylim = np.log10(ylim)

            log_xrange = max(log_xlim) - min(log_xlim) 
            log_yrange = max(log_ylim) - min(log_ylim) 

            # Check whether the two points are too close 
            if x_sep < min_x_fractional_sep*log_xrange and y_sep < min_y_fractional_sep*log_yrange:
                return True
            else: 
                return False  


        # Decide which points to include labels for 
        indices_plotted = [0]
        for i in np.arange(1, len(logx)): 
            too_close = calc_is_too_close((logx[indices_plotted[-1]],logy[indices_plotted[-1]]), (logx[i],logy[i]), (self.ax.get_xlim(), self.ax.get_ylim()))
            if too_close == False: 
                indices_plotted.append(i) 


        # Plot points 
        self.ax.scatter(
            10**logx[indices_plotted], 
            10**logy[indices_plotted], 
            zorder=30, 
            color="black", 
            s=20 
        ) 

        # Plot text labels 
        for ind in indices_plotted:
            self.ax.annotate(
                labels[ind],
                xy=(10**logx[ind], 10**logy[ind]),          
                xytext=(0, 15), 
                textcoords="offset points", 
                fontsize=9,
                weight="bold",
                ha='center',
                va='bottom',
                zorder=20,

                bbox=dict(
                    facecolor='white',
                    edgecolor='black',
                    alpha=0.5,
                    boxstyle='round,pad=0.2'
                ),

                arrowprops=dict(
                    arrowstyle='-|>',
                    color='black', 
                )
            )



