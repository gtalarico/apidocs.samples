using System.Reflection;
using System.Runtime.InteropServices;

// General Information about an assembly is controlled through the following
// set of attributes. Change these attribute values to modify the information
// associated with an assembly.
[assembly: AssemblyTitle( "Revit ExportCncFab Add-In" )]
[assembly: AssemblyDescription( "Revit Add-In to export Revit wall parts to DXF or SAT for CNC fabrication" )]
[assembly: AssemblyConfiguration( "" )]
[assembly: AssemblyCompany( "Autodesk Inc." )]
[assembly: AssemblyProduct( "Revit ExportCncFab Add-In" )]
[assembly: AssemblyCopyright( "Copyright 2013-2021 (C) Jeremy Tammik Autodesk Inc." )]
[assembly: AssemblyTrademark( "" )]
[assembly: AssemblyCulture( "" )]

// Setting ComVisible to false makes the types in this assembly not visible
// to COM components.  If you need to access a type in this assembly from
// COM, set the ComVisible attribute to true on that type.
[assembly: ComVisible( false )]

// The following GUID is for the ID of the typelib if this project is exposed to COM
[assembly: Guid( "118f7279-630d-4661-afe5-c23c23acf46f" )]

// Version information for an assembly consists of the following four values:
//
//      Major Version
//      Minor Version
//      Build Number
//      Revision
//
// You can specify all the values or you can default the Build and Revision Numbers
// by using the '*' as shown below:
// [assembly: AssemblyVersion("1.0.*")]
//
// 2015-06-16 2015.0.0.0 flat migration to Revit 2015
// 2015-06-16 2015.0.0.1 removed all obsolete API usage, compile with zero warnings
// 2015-06-16 2015.0.0.2 fixed post-build event
// 2015-06-16 2016.0.0.0 flat migration to Revit 2016
// 2017-05-03 2017.0.0.0 flat migration to Revit 2017
// 2017-05-03 2018.0.0.0 flat migration to Revit 2018
// 2018-01-11 2018.0.0.1 incremented copyright year to 2018
// 2018-10-16 2019.0.0.0 flat migration to Revit 2019
// 2020-12-01 2020.0.0.0 flat migration to Revit 2020
// 2020-12-01 2021.0.0.0 flat migration to Revit 2021
// 2020-12-01 2021.0.0.1 added support for CncFabSortMark shared parameter
// 2021-09-02 2022.0.0.0 flat migration to Revit 2022
// 2021-09-02 2022.0.0.1 eliminated deprecated API usage of ParameterType and some unused namespaces
//
[assembly: AssemblyVersion( "2022.0.0.1" )]
[assembly: AssemblyFileVersion( "2022.0.0.1" )]
