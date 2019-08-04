The Mathematics Genealogy Project: 
Where Did I Come From (Mathematically)?
    
Michael J. Carlisle, Ph.D.

The primary intent of this project is to create a method for simplified exploration and visualization of the data in the Mathematics Genealogy Project (MGP), located at https://genealogy.math.ndsu.nodak.edu/index.php, a project of North Dakota State University's Department of Mathematics, which has since 1995 been cataloging those individuals who have earned (the equivalent of, historically) a doctorate in mathematics, through the lineage of the "advisor/advisee" relationship.

At the outset, we would like to address some potential issues with the data used in this project. See the MGP's mission statement at https://genealogy.math.ndsu.nodak.edu/mission.php for details. As the data purports to extend back to the 13th Century (CE), there are not only historical idiosyncracies to address, but some "smoothing" of the available data to allow exploration through time.

The data sets used in this project come from:
 * Mathematics Genealogy Project (MGP) (https://genealogy.math.ndsu.nodak.edu/index.php)
 * Mathematics Subject Classification (MSC) 2010 (http://msc2010.org/Default.html)
 * Google Geocode API (https://developers.google.com/maps/documentation/geocoding/start)
 
The programming tools and APIs used in this project are: 
 * Python
 * Matplotlib
 * NumPy
 * Pandas
 * scikit-learn
 * NLTK
 * Basemap
 * Google Geocode API
 * FFMPEG
 * Bokeh
 * Plotly Express
 
There are several aspects to this project. Some notes about the files here:
 * The .mp4 files demonstrate #2 and #7.
 * What MSC are you?.ipynb and its associated code demonstrate #3. (The model itself is not on Github.)
 * visualizations.ipynb contains graphs from #4 and #6.

0. Clean the data of the MGP to enable analysis and visualizations.
1. Collect geographic data (from Google Geocode API) on as many of the schools in the MGP as possible to enable map-based visualizations.
2. Using the Geocode data from #1, build visualizations to track the progress of mathematical thought across the globe over time, using Basemap (https://matplotlib.org/basemap/) and FFMPEG (https://ffmpeg.org/).
3. Use NLP to accurately classify a mathematics thesis title via the MSC, to fill in the missing MSC codes in the MGP, and enable the data set available for plotting to be larger. Create a text-based input to classify user-input text into the MSC (after being trained on these titles and the MSC topics).
4. Use the newly-classified thesis titles from #3 to build a visualization of categorizations across years and across countries.
5. Use NLP clustering to reclassify theses, using the MSC as a guide, into smaller numbers of categories. 
6. Build a visualization that displays the clustering in #5, and another that compares the relative sizes of two or more collections of theses/degrees (via individual MSC codes, or some other paramater(s)).
7. Make it personal: I am interested in mapping my own lineage, to see the geographic and subject landscape of my own mathematical history.

NOTE: Jupyter notebooks given here are not supplied with the data supplied by the MGP, nor with most of the pickled data generated during the project. Code is here for purposes of documenting the project.
