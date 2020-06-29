# Diameter-Polytopes
Supplementary Material for Diameter Polytopes of Feasible Binary Programs
## Authors
* [Thomas R. Cameron](https://thomasrcameron.com)
	* Mathematics Department, Penn State Behrend
	* [Email: trc5475@psu.edu](mailto:trc5475@psu.edu)
* [Sebastian Charmot]
	* [Email: secharmot@davidson.edu](mailto:secharmot@davidson.edu)
* [Jonad Pulaj](https://jonadpulaj.com)
	* Mathematics and Computer Science Department, Davidson College
	* [Email: jopulaj@davidson.edu](mailto:jopulaj@davidson.edu)
	
## Instructions
This repo contains python code for generating points and facets for the diameter polytope of the linear ordering problem and the symmetric traveling salesman problem, in files lod_point_facet_gen.py and tsd_point_facet_gen.py, respectively. In addition, a full python implementation of the diameter binary program of the linear ordering problem is included in lop_opt_dia.py. 
### Point and Facet Generator
The files lod_point_facet_gen.py and tsd_point_facet_gen.py accept two parameters: n and t, where n denotes the size of the problem and t denotes the type of the problem (p for points and f for facets). For example, the command python lod_point_facet_gen.py 3 p would create a .poly file containing all points for the diameter polytope of the linear ordering problem when n=3. The .poly file is formated so that it can be loaded into polymake. Once in polymake, the user can investigate the polytope described by the given points. In particular, one can save all facet inequalities, e.g., see the facet files in the point_facet_files directory. 
### Diameter LOP Implementation
The diameter binary program for the linear ordering problem is implemented in the lop_opt_dia.py. In particular, given an objective function stored as a nxn matrix, the function lopOptDia returns the optimal diameter and two optima that are as diverse as possible. The main function demonstrates the use of this function on several examples and displays the diverse optimal rankings in parallel.