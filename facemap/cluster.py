import umap
import numpy as np
from PyQt5 import QtGui, QtCore
import pyqtgraph as pg
import pyqtgraph.opengl as gl
from sklearn.cluster import MiniBatchKMeans
import hdbscan
from matplotlib import cm
from . import io

def create_clustering_widgets(parent):
    parent.cluster_labels = None
    # Add options to change params for embedding using user input
    parent.ClusteringLabel = QtGui.QLabel("Clustering")
    parent.ClusteringLabel.setStyleSheet("color: white;")
    parent.ClusteringLabel.setAlignment(QtCore.Qt.AlignCenter)
    parent.ClusteringLabel.setFont(QtGui.QFont("Arial", 12, QtGui.QFont.Bold))
    
    parent.min_dist_label = QtGui.QLabel("min_dist:")
    parent.min_dist_label.setStyleSheet("color: gray;")
    parent.min_dist_value = QtGui.QLineEdit()
    parent.min_dist_value.setText(str(0.5))
    parent.min_dist_value.setFixedWidth(50)

    parent.n_neighbors_label = QtGui.QLabel("n_neighbors:")
    parent.n_neighbors_label.setStyleSheet("color: gray;")
    parent.n_neighbors_value = QtGui.QLineEdit()
    parent.n_neighbors_value.setText(str(30))
    parent.n_neighbors_value.setFixedWidth(50)

    parent.n_components_label = QtGui.QLabel("n_components:")
    parent.n_components_label.setStyleSheet("color: gray;")
    parent.n_components_value = QtGui.QSpinBox()
    parent.n_components_value.setRange(2, 3)
    parent.n_components_value.setValue(2)
    parent.n_components_value.setFixedWidth(50)
    #metric

    parent.cluster_method_label = QtGui.QLabel("Cluster labels")
    parent.cluster_method_label.setStyleSheet("color: gray;")
    parent.cluster_method_label.setAlignment(QtCore.Qt.AlignCenter)

    parent.load_cluster_labels_button = QtGui.QPushButton('Load')
    parent.loadlabels_radiobutton = QtGui.QRadioButton("Load labels")
    parent.loadlabels_radiobutton.setStyleSheet("color: gray;")
    parent.kmeans_radiobutton = QtGui.QRadioButton("KMeans")
    parent.kmeans_radiobutton.setStyleSheet("color: gray;")
    parent.hdbscan_radiobutton = QtGui.QRadioButton("HDBSCAN")
    parent.hdbscan_radiobutton.setStyleSheet("color: gray;")

    parent.min_cluster_size_label = QtGui.QLabel("min_cluster_size:")
    parent.min_cluster_size_label.setStyleSheet("color: gray;")
    parent.min_cluster_size = QtGui.QLineEdit()
    parent.min_cluster_size.setFixedWidth(50)
    parent.min_cluster_size.setText(str(500))

    parent.num_clusters_label = QtGui.QLabel("num_clusters:")
    parent.num_clusters_label.setStyleSheet("color: gray;")
    parent.num_clusters = QtGui.QLineEdit()
    parent.num_clusters.setFixedWidth(50)
    parent.num_clusters.setText(str(5))

    istretch = 15
    parent.l0.addWidget(parent.ClusteringLabel, istretch, 0, 1, 2)
    parent.l0.addWidget(parent.min_dist_label, istretch+1, 0, 1, 1)
    parent.l0.addWidget(parent.min_dist_value, istretch+1, 1, 1, 1)
    parent.l0.addWidget(parent.n_neighbors_label, istretch+2, 0, 1, 1)
    parent.l0.addWidget(parent.n_neighbors_value, istretch+2, 1, 1, 1)
    parent.l0.addWidget(parent.n_components_label, istretch+3, 0, 1, 1)
    parent.l0.addWidget(parent.n_components_value, istretch+3, 1, 1, 1)
    parent.l0.addWidget(parent.cluster_method_label, istretch+4, 0, 1, 2)
    parent.l0.addWidget(parent.loadlabels_radiobutton, istretch+5, 0, 1, 1)
    parent.l0.addWidget(parent.load_cluster_labels_button, istretch+5, 1, 1, 1)
    parent.l0.addWidget(parent.kmeans_radiobutton, istretch+6, 0, 1, 1)
    parent.l0.addWidget(parent.hdbscan_radiobutton, istretch+6, 1, 1, 1)
    parent.l0.addWidget(parent.min_cluster_size_label, istretch+7, 0, 1, 1)
    parent.l0.addWidget(parent.min_cluster_size, istretch+7, 1, 1, 1)
    parent.l0.addWidget(parent.num_clusters_label, istretch+7, 0, 1, 1)
    parent.l0.addWidget(parent.num_clusters, istretch+7, 1, 1, 1)

    hide_umap_param(parent)
    parent.loadlabels_radiobutton.toggled.connect(lambda: show_cluster_method_param(parent))
    parent.kmeans_radiobutton.toggled.connect(lambda: show_cluster_method_param(parent))
    parent.hdbscan_radiobutton.toggled.connect(lambda: show_cluster_method_param(parent))
    parent.load_cluster_labels_button.clicked.connect(lambda: io.load_cluster_labels(parent))

def enable_data_clustering_features(parent):
    parent.data_clustering_combobox.clear()
    parent.ClusteringPlot.clear()
    # Add data to be used for clustering
    parent.data_clustering_combobox.addItem("-- Data --")
    data_types = ["motion SVD", "Running", "Pupil", "Blink"]
    data = [parent.motSVDs[0], parent.running, parent.pupil, parent.blink]
    for i in range(len(data_types)):
        if len(data[i]) > 0:
            parent.data_clustering_combobox.addItem(data_types[i])
    parent.data_clustering_combobox.setCurrentIndex(0)
    parent.data_clustering_combobox.show()
    parent.run_clustering_button.show()

    cluster_method = parent.clusteringVisComboBox.currentText()
    if cluster_method == "UMAP":
        parent.data_clustering_combobox.show()
        show_umap_param(parent)
    else:
        disable_data_clustering_features(parent)

def disable_data_clustering_features(parent):
    parent.data_clustering_combobox.hide()
    parent.ClusteringPlot.clear()
    hide_umap_param(parent)
    parent.run_clustering_button.hide()

def show_umap_param(parent):
    parent.ClusteringLabel.show()
    parent.min_dist_label.show()
    parent.min_dist_value.show()
    parent.n_neighbors_label.show()
    parent.n_neighbors_value.show()
    parent.n_components_label.show()
    parent.n_components_value.show()
    parent.cluster_method_label.show()
    parent.loadlabels_radiobutton.show()
    parent.kmeans_radiobutton.show()
    parent.hdbscan_radiobutton.show()
    show_cluster_method_param(parent)

def hide_umap_param(parent):
    parent.ClusteringLabel.hide()
    parent.min_dist_label.hide()
    parent.min_dist_value.hide()
    parent.n_neighbors_label.hide()
    parent.n_neighbors_value.hide()
    parent.n_components_label.hide()
    parent.n_components_value.hide()
    parent.cluster_method_label.hide()
    parent.load_cluster_labels_button.hide()
    parent.loadlabels_radiobutton.hide()
    parent.kmeans_radiobutton.hide()
    parent.hdbscan_radiobutton.hide()
    parent.num_clusters_label.hide()
    parent.num_clusters.hide()
    parent.min_cluster_size_label.hide()
    parent.min_cluster_size.hide()

def show_cluster_method_param(parent):
    if parent.loadlabels_radiobutton.isChecked():
        parent.min_cluster_size_label.hide()
        parent.min_cluster_size.hide()
        parent.num_clusters_label.hide()
        parent.num_clusters.hide()
        parent.load_cluster_labels_button.show()
    elif parent.kmeans_radiobutton.isChecked():
        parent.min_cluster_size_label.hide()
        parent.min_cluster_size.hide()
        parent.load_cluster_labels_button.hide()
        parent.num_clusters_label.show()
        parent.num_clusters.show()
    elif parent.hdbscan_radiobutton.isChecked():
        parent.num_clusters_label.hide()
        parent.num_clusters.hide()
        parent.load_cluster_labels_button.hide()
        parent.min_cluster_size_label.show()
        parent.min_cluster_size.show()
    else:
        return

def get_cluster_labels(data, parent):
    try:
        if parent.kmeans_radiobutton.isChecked():
            num_clusters = int(parent.num_clusters.text())
            kmeans = MiniBatchKMeans(n_clusters=num_clusters, tol=1e-3, 
                            batch_size=100, max_iter=50)
            kmeans.fit(data)
            parent.cluster_labels = kmeans.labels_
        elif parent.hdbscan_radiobutton.isChecked():
            clusterer = hdbscan.HDBSCAN(min_cluster_size=int(parent.min_cluster_size.text())).fit(data)
            parent.cluster_labels = clusterer.labels_
        else:
            return
    except Exception:
        QtGui.QMessageBox.about(parent, 'Error','Parameter input can only be a number')
        pass

def get_colors(parent):
    num_classes = len(np.unique(parent.cluster_labels))
    colors = cm.get_cmap('gist_rainbow')(np.linspace(0, 1., num_classes))
    colors *= 255
    colors = colors.astype(int)
    colors[:,-1] = 127
    brushes = [pg.mkBrush(color=c) for c in colors]
    return brushes

def run(clicked, parent):
    parent.clear_visualization_window()
    user_selection = parent.data_clustering_combobox.currentText()
    if user_selection == "motion SVD":
        data = parent.motSVDs[0]       # Shape: num frames x num comps
    elif user_selection == "Pupil":
        data = parent.pupil
    elif user_selection == "Blink":
        data = parent.blink
    elif user_selection == "Running":
        data = parent.running
    else:
        msg = QtGui.QMessageBox(parent)
        msg.setIcon(QtGui.QMessageBox.Warning)
        msg.setText("Please select data for clustering")
        msg.setStandardButtons(QtGui.QMessageBox.Ok)
        msg.exec_()
        return
    cluster_method = parent.clusteringVisComboBox.currentText()
    if cluster_method == "UMAP":
        parent.update_status_bar("Clustering using "+str(cluster_method))
        plot_clustering_output(umap_embedding(data, parent), parent)
        parent.update_status_bar("Clustering done!")
    else:
        hide_umap_param(parent)

def umap_embedding(data, parent):
    """
    This function uses UMAP to embed loaded/processed SVD output
    """
    num_feat = data.shape[0]     # number of frames
    num_comp = data.shape[1]     # number of PCs usually 500
    try: 
        standard_embedding = umap.UMAP(n_neighbors=int(parent.n_neighbors_value.text()), 
                        min_dist=float(parent.min_dist_value.text()),
                        n_components=int(parent.n_components_value.value())).fit_transform(data) # cluster features/frames
        return standard_embedding
    except Exception:
        QtGui.QMessageBox.about(parent, 'Error','Parameter input can only be a number')
        pass

def plot_clustering_output(embedded_output, parent):
    num_feat = embedded_output.shape[0]
    num_comps = embedded_output.shape[1]
    is_cluster_colored = False
    # Get cluster labels if clustering method selected for embedded output
    if parent.kmeans_radiobutton.isChecked() or parent.hdbscan_radiobutton.isChecked() or parent.loadlabels_radiobutton.isChecked():
        get_cluster_labels(embedded_output, parent)
        brushes = get_colors(parent)
        name = parent.cluster_labels
        is_cluster_colored = True
    else:
        all_spots_colors = [pg.mkBrush(color='w') for i in range(num_feat)]
        name = None
    
    # Plot output (i) w/ cluster labels (ii) w/o  cluster labels and (iii) 3D output
    if num_comps == 2:
        if is_cluster_colored:
            scatter_plots = []
            if max(parent.cluster_labels) > 4:
                legend_num_row = 4
                legend_num_col = int(np.ceil(max(parent.cluster_labels)/legend_num_row))+1
            else:
                legend_num_col, legend_num_row = [1, 1]
            parent.ClusteringPlot_legend = pg.LegendItem(labelTextSize='12pt', horSpacing=12,
                                                         colCount=legend_num_col, rowCount=legend_num_row)
            for cluster in range(max(parent.cluster_labels)+1):
                ind = np.where(parent.cluster_labels==cluster)[0]
                data = embedded_output[ind,:]
                scatter_plots.append(pg.ScatterPlotItem(data[:,0], data[:,1], symbol='o', brush=brushes[cluster],
                                            hoverable=True, hoverSize=15, data=ind, name=str(cluster)))
                parent.ClusteringPlot.addItem(scatter_plots[cluster])
                parent.ClusteringPlot_legend.addItem(scatter_plots[cluster], name=str(cluster))
            # Add all points (transparent) to connect them to hovered function
            parent.clustering_scatterplot.setData(embedded_output[:,0], embedded_output[:,1], symbol='o', brush=(0,0,0,0),
                                            hoverable=True, hoverSize=15, pen=(0,0,0,0), data=np.arange(num_feat),name=name)
            parent.ClusteringPlot.addItem(parent.clustering_scatterplot)
            parent.ClusteringPlot_legend.setPos(parent.clustering_scatterplot.x()+5,parent.clustering_scatterplot.y())
            parent.ClusteringPlot_legend.setParentItem(parent.ClusteringPlot)
        else:
            parent.clustering_scatterplot.setData(embedded_output[:,0], embedded_output[:,1], symbol='o', brush=all_spots_colors,
                                            hoverable=True, hoverSize=15, data=np.arange(num_feat),name=name)
            parent.ClusteringPlot.addItem(parent.clustering_scatterplot)
        parent.ClusteringPlot.showAxis('left')
        parent.ClusteringPlot.showAxis('bottom')
        parent.ClusteringPlot.setLabels(bottom='UMAP coordinate 1',left='UMAP coordinate 2') 
    else: # 3D embedded visualization
        view = gl.GLViewWidget()
        view.setWindowTitle("3D plot of embedded points")
        plot = gl.GLScatterPlotItem()
        plot.setData(pos=embedded_output)
        axis = gl.GLAxisItem()
        axis.setSize(x= max(embedded_output[:,0]),y= max(embedded_output[:,1]),z= max(embedded_output[:,2]))
        view.addItem(plot)
        view.addItem(axis)
        #view.setMouseTracking(True)
        #view.mousePressEvent(ev)
        view.show()

def mousePressEvent(self, ev):
    super().mousePressEvent(ev)
    print(self.mousePos)
   # self.mousePos = ev.pos()

def embedded_points_hovered(obj, ev, parent):
    point_hovered = np.where(parent.clustering_scatterplot.data['hovered'])[0]
    if point_hovered.shape[0] >= 1:         # Show tooltip only when hovering over a point i.e. no empty array
        points = parent.clustering_scatterplot.points()
        vb = parent.clustering_scatterplot.getViewBox()
        if vb is not None and parent.clustering_scatterplot.opts['tip'] is not None:
            cutoff = 1                      # Display info of only one point when hovering over multiple points
            tip = [parent.clustering_scatterplot.opts['tip'](data = points[pt].data(),x=points[pt].pos().x(), y=points[pt].pos().y())
                    for pt in point_hovered[:cutoff]]
            if len(point_hovered) > cutoff:
                tip.append('({} other...)'.format(len(point_hovered) - cutoff))
            vb.setToolTip('\n\n'.join(tip))
            frame = str(points[point_hovered[0]].data())
            parent.setFrame.setText(frame)                # display frame from one of the hovered points
