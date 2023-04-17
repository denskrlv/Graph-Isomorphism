# Graph Isomorphism
Graph Isomorphism project by:<br/>
Team 70<br/>
Denis Krylov s2808757<br/> 
Yulin Chen s2845024<br/>
Paul Florian s2716682<br/>


# How to run the program

Format graphs in **.gr/.grl** file types. Copy those graphs to directory **"Graph-Isomorphisms-70/graphs"**. 
* For solving the GI problem, add substring "GI" to the filename, the name should not contain the substring "Aut". (example: "cubes6GI.grl")
* For solving the #Aut problem, add substring "Aut" to the filename, the name should not contain the substring "GI". (example: "trees3Aut.gr")
* For solving both GI and #Aut problems, add substring "GIAut" to the filename. (example: "torus144GIAut.grl")

After that, run **"main.py"** in directory **"Graph-Isomorphisms-70"** and all the graph files in the **"graphs"** directory will be processed and the results will be printed on screen.


# Project Structure
***Directories***<br/>
framework: files provided by the University + main program for processing graphs<br/>
utils: self-written utility functions for processing graphs<br/>

***Important files***<br/>
main.py: executable python file which processes input files and produces the desired output.<br/>
graph_analyzer.py: main program for performing partition refinement, branching and computing automorphism groups.

# How to select instances
1. Copy the instance files (.gr/.grl) to directory "Graph-Isomorphisms-70/graphs" and follow the naming scheme mentioned above in "How to run the program".
2. Run main.py, the user does not need to input anything as only the instances in the graphs directory will be processed.