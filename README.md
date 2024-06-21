PyCell Enhancements by He Zeng. Usage Instructions: Place the Python and tech files in the local KLayout directory. Then, load the .lyp file in KLayout

This document provides an overview of the classes and methods that have been added or modified by He Zeng, based on the code from IHP OpenPDK. 
## Added and Modified Classes and Methods
### Classes and the Number of Methods Added

1.  **Box**: 91 methods
2.  **Direction**: 21 methods
3.  **Grouping**: 19 methods
4.  **Grid**: 11 methods
5.  **Instance**: 12 methods
6.  **Donut**: 15 methods
7.  **Rect**: 39 methods
8.  **Dot**: 8 methods
9.  **Orientation**: 2 methods
10. **ParamArray**: 16 methods
11. **Path**: 9 methods
12. **Pin**: 6 methods
13. **Point**: 32 methods
14. **PointList**: 12 methods
15. **Polygon**: 20 methods
16. **Range**: 36 methods
17. **RangeConstraint**: 2 methods
18. **ShapeFilter**: 5 methods
19. **SnapType**: 6 methods
20. **StepConstraint**: 2 methods
21. **Text**: 12 methods
22. **Transform**: 9 methods
23. **UList**: 12 methods
24. **Arc**: 8 methods
25. **Segmenter**: 24 methods
26. **ChoiceConstraint**: 2 methods
27. **NameMapper**: 2 methods
28. **Layer**: 4 methods added (the remaining methods are from IHP OpenPDK)
29. **Numeric**: 5 methods added (the remaining methods are from IHP OpenPDK)
30. **Shape**:10 methods added(the remaining methods are from IHP OpenPDK)
31. **Dlo**: 2 methods added (the remaining methods are from IHP OpenPDK)
32. **Tech**: 1 method addded (the remaining methods are from IHP OpenPDK)

### 
Based on the code provided by IHP OpenPDK, the following classes have been modified to include additional functionalities:
1. PyCellWrapper class: Modified the `__call__` method and `coerce_parameters` method, modified the `PyCellContext` class，and adapted some methods and descriptors from the KLayout main source.
2. All PyCells and technology files(.lyp and .lyt files) are provided by IHP OpenPDK, the module sg13g2_pycell_lib is from IHP OpenPDK.
3. using a KLayout macro file to automatically register the PyCellLib library; the PyCellLib class is from IHP OpenPDK.
4. The file sg13_tech.py is from IHP OpenPDK, He Zeng make some change based on the documentation from IHP OPenPDK.

## Usage Notes:
1.Be aware that there are issues with the original code for `npn13G2L` and `npn13G2V` PyCells. Specific problems can be identified in the corresponding PyCell code.
2.In KLayout, PyCells are automatically registered (using the .lym macro file) and should not be run again; doing so may cause issues.
This is because the variable `Layer.tech` is automatically set to `None` after the first run, 
preventing further retrieval of information related to `Layer`. If this happens, KLayout must be restarted.
3.In subsequent development of new classes, `importlib` with a reload function will need to be used multiple times. 
The main reason is that KLayout embeds Python interpreter, which do not automatically re-execute files.

 


