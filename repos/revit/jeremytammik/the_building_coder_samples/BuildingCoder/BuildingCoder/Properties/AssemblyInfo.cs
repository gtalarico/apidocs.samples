﻿using System.Reflection;
using System.Runtime.CompilerServices;
using System.Runtime.InteropServices;

// General Information about an assembly is controlled through the following
// set of attributes. Change these attribute values to modify the information
// associated with an assembly.
[assembly: AssemblyTitle( "BuildingCoder" )]
[assembly: AssemblyDescription( "The Building Coder samples, http://thebuildingcoder.typepad.com" )]
[assembly: AssemblyConfiguration( "" )]
[assembly: AssemblyCompany( "Autodesk, Inc." )]
[assembly: AssemblyProduct( "BuildingCoder" )]
[assembly: AssemblyCopyright( "Copyright © 2008-2019 by Jeremy Tammik, Autodesk, Inc." )]
[assembly: AssemblyTrademark( "" )]
[assembly: AssemblyCulture( "" )]

// Setting ComVisible to false makes the types in this assembly not visible
// to COM components.  If you need to access a type in this assembly from
// COM, set the ComVisible attribute to true on that type.
[assembly: ComVisible( false )]

// The following GUID is for the ID of the typelib if this project is exposed to COM
[assembly: Guid( "15d5844d-8236-48dc-ad63-7ce8f99dec10" )]

// Version information for an assembly consists of the following four values:
//
//      Major Version
//      Minor Version
//      Build Number
//      Revision
//
// You can specify all the values or you can default the Revision and Build Numbers
// by using the '*' as shown below:
// 2014-04-11 2014.0.109.0 renamed CmdSlopedFloor.cs to CmdCreateSlopedSlab.cs, implemented CmdCategorySupportsTypeParameter
// 2014-04-14 2015.0.109.0 migrated to Revit 2015
// 2014-05-14 2015.0.110.0 CmdViewsShowingElements
// 2014-07-21 2015.0.110.1 AddFaceBasedFamilyToLinks
// 2014-08-19 2015.0.110.2 removed obsolete API usage: reduced warning count from 71 to 67
// 2014-08-20 2015.0.110.3 added code in CmdUnrotateNorth to determine angle to north from project base point
// 2014-08-20 2015.0.111.0 implemented CmdDocumentVersion
// 2014-08-27 2015.0.111.1 cleaned up PickFaceSetWorkPlaneAndPickPoint, implemented PickPointsForArea, Plane ProjectOnto and ProjectInto extension methods
// 2014-09-01 2015.0.111.2 documented CmdPickPoint3d and added Autodesk.Revit.Exceptions namespace prefix to all uses of OperationCanceledException
// 2014-09-01 2015.0.111.3 added notes on NewFloor refusing floor types that are foundation slab types
// 2014-09-29 2015.0.112.0 implemented CmdNewExtrusionRoof
// 2014-10-01 2015.0.113.0 implemented CmdFaceWall
// 2014-10-01 2015.0.113.1 skip horizontal faces
// 2014-10-06 2015.0.113.2 implemented IsElementHiddenInView
// 2014-10-11 2015.0.114.0 implemented CmdNewTextNote
// 2014-10-11 2015.0.114.1 CmdNewTextNote text width enhancements suggested by Scott Wilson
// 2014-10-15 2015.0.114.2 CmdNewTextNote reimplementation based on Graphics.MeasureString instead of TextRenderer.MeasureText suggested by Scott Wilson
// 2014-10-16 2015.0.114.3 added pipe wall thickness determination to CmdRollingOffset
// 2014-10-11 2015.0.115.0 implemented CmdNewCrossFitting
// 2014-10-11 2015.0.115.1 fixed some of the warnings about deprecated use of Selection.Elements collection
// 2014-11-10 2015.0.115.2 converted CmdNewSweptBlend to use manual transaction mode and implemented CreateNewSweptBlendArc
// 2014-11-11 2015.0.116.0 implemented CmdDimensionInstanceOrigin and JtPairPicker
// 2014-11-12 2015.0.116.1 replace explicit selection code in CmdRollingOffset by new JtPairPicker class
// 2014-11-12 2015.0.116.3 implement generic JtElementsOfClassSelectionFilter template class
// 2014-11-12 2015.0.116.3 replace explicit Wall, CurveElement and Pipe selection filters by JtElementsOfClassSelectionFilter
// 2014-11-13 2015.0.116.4 eliminated obsolete API usage warning in CmdCollectorPerformance.cs: replace get_Parameter(string) by built-in enumeration value
// 2014-11-13 2015.0.116.4 eliminated obsolete API usage warning in CmdCollectorPerformance.cs: use Pipe.Create instead of doc.Create.NewPipe
// 2014-11-13 2015.0.116.4 eliminated obsolete API usage warning in CmdCoordsOfViewOnSheet.cs: use GetAllPlacedViews() instead of Autodesk.Revit.DB.ViewSheet.Views
// 2014-11-13 2015.0.116.4 eliminated various obsolete API usage warnings saying Autodesk.Revit.UI.Selection.Selection.Elements is obsolete: Use GetElementIds instead
// 2014-11-14 2015.0.116.5 implemented GetInstancesIntersectingElement
// 2014-11-14 2015.0.116.5 radical rewrite of SelectSingleElement, GetSingleSelectedElement, GetSelectedElementsOrAll to clean up and eliminate obsolete API usage
// 2014-11-14 2015.0.116.5 radical rewrite of HasRequestedType, which probably never previously worked as intended
// 2014-11-19 2015.0.116.6 implemented GetSortedLevels
// 2015-01-27 2015.0.116.7 added second implementation to CmdWallProfile
// 2015-01-27 2015.0.116.8 updated copyright year to 2015
// 2015-01-27 2015.0.116.9 eliminated obsolete API usage, 15 warnings left
// 2015-01-27 2015.0.117.0 implemented CmdListPipeSizes
// 2015-02-09 2015.0.117.1 implemented mechanism to abort PromptForFamilyInstancePlacement after placing first instance
// 2015-02-10 2015.0.117.2 eliminated all deprecated API usage to compile with zero warnings now
// 2015-02-14 2015.0.117.3 implemented PlaceFamilyInstanceOnFace
// 2015-02-19 2015.0.117.4 updated CmdInstallLocation from Revit 2010 to 2015 and replaced TransactionMode.Automatic by ReadOnly
// 2015-02-20 2015.0.117.5 updated CmdListMarks to use TransactionMode.Manual instead of Automatic
// 2015-02-20 2015.0.118.0 implemented CmdItemExecuted and added reference to PresentationFramework assembly
// 2015-03-02 2015.0.119.0 implemented CmdPostRequestInstancePlacement
// 2015-03-03 2015.0.119.1 implemented HideLightingFixtureHosts
// 2015-03-11 2015.0.119.2 implemented sketch for traversing family instances per level and category
// 2015-03-11 2015.0.119.2 replaced automatic transaction mode by manual in CmdWallProfileArea
// 2015-03-11 2015.0.119.2 replaced automatic transaction mode by manual in CmdWallLayers
// 2015-03-11 2015.0.119.2 replaced automatic transaction mode by read-only in CmdWallDimensions
// 2015-03-11 2015.0.120.0 implemented CmdSelectionChanged
// 2015-03-25 2015.0.120.1 added Revit 2015 API class diagram
// 2015-03-25 2015.0.120.2 renamed class diagram adding Revit.DB namespace
// 2015-03-25 2015.0.120.3 before Alexander Ignatovich ai CmdWallProfile enhancement
// 2015-03-25 2015.0.120.4 integrated Alexander Ignatovich ai CmdWallProfile - first attempt.cs
// 2015-03-25 2015.0.120.5 integrated Alexander Ignatovich ai CmdWallProfile - second attempt.cs
// 2015-03-25 2015.0.120.6 integrated Alexander Ignatovich ai CmdWallProfile - final.cs
// 2015-03-25 2015.0.120.7 eliminated and replaced non-static Creator.CreateModelLine taking XYZ start and end point by static overload taking Document as well
// 2015-04-13 2015.0.120.9 implemented Plane Compare method
// 2015-05-05 2015.0.120.10 cleaned up, tested and fixed a bug in CmdCopyWallType
// 2015-05-15 2015.0.120.11 started integrating version compatibility extension methods by Magson Leone
// 2015-05-18 2015.0.120.12 second attempt at integrating version compatibility extension methods by Magson Leone
// 2015-05-19 2015.0.120.13 third version of version compatibility extension methods by Magson Leone
// 2015-05-20 2016.0.120.0 first successful compilation for the Revit 2016 API
// 2015-05-26 2016.0.120.1 updated BcSamples.txt for Revit 2016 and implemented Util.Intersection method
// 2015-05-27 2016.0.120.2 enhanced Util.Intersection to gracefully handle parallel or coincident lines
// 2015-07-08 2016.0.120.3 added solid sphere and cube creation utility methods
// 2015-07-13 2016.0.120.4 added super simple floor creation code
// 2015-08-13 2016.0.120.5 added SetSiteLocationToCity2
// 2015-08-18 2016.0.120.6 removed obsolete API usage in CmdNewLineLoad.cs
// 2015-08-18 2016.0.120.7 removed obsolete API usage in CmdCollectorPerformance, CmdCreateSlopedSlab, CmdNewTextNote, CmdRoomNeighbours, CmdRoomWallAdjacency, and CmdSpaceAdjacency
// 2015-08-18 2016.0.120.8 replaced obsolete PlanarFace.Normal property by PlanarFace.FaceNormal
// 2015-08-18 2016.0.120.9 eliminated obsolete API calls to ElementTransformUtils.MirrorElements by adding bool mirrorCopies argument
// 2015-09-04 2016.0.120.10 added original EditFilledRegion to show code improvements
// 2015-09-04 2016.0.120.11 in EditFilledRegion: foreach iter, using tx, single tx, XYZ static member
// 2015-09-04 2016.0.120.12 in EditFilledRegion: use MoveElements instead of MoveElement
// 2015-09-14 2016.0.120.14 implemented GetAllModelElements
// 2015-09-14 2016.0.120.15 implemented IterateOverCollector
// 2015-09-28 2016.0.120.16 added rof creation sample code from Revit online help sample
// 2015-10-20 2016.0.121.0 implemented CmdSheetToModel using code provided by Paolo Serra
// 2015-10-22 2016.0.121.1 added miros sample code
// 2015-10-30 2016.0.121.2 implemented Util.NewExternalDefinitionCreationOptions method
// 2015-10-31 2016.0.121.3 implemented SpellingErrorCorrector
// 2015-11-05 2016.0.122.0 implemented CmdSetWallType
// 2015-11-05 2016.0.122.1 implemented GetAllDetailComponentCustomParamValues
// 2015-11-16 2016.0.123.0 implemented CmdFlatten
// 2015-11-29 2016.0.123.1 updated CmdDetailCurves to create detail curve along pre-selected wall centre location curve
// 2015-11-30 2016.0.123.2 YbExporteContext
// 2015-12-16 2016.0.124.0 implemented CmdWallOpenings
// 2015-12-17 2016.0.125.0 integrated CmdProjectParameterGuids by CoderBoy
// 2015-12-17 2016.0.125.1 cleaned up CmdWallOpenings
// 2015-12-18 2016.0.125.2 cleaned up CmdProjectParameterGuids
// 2015-12-22 2016.0.126.0 integrated CmdWallOpeningProfiles by Scott Wilson
// 2015-12-22 2016.0.126.1 cleaned up for publication
// 2016-01-08 2016.0.126.2 incremented copyright year
// 2016-02-24 2016.0.126.3 implemented CmdMepElementShape.GetElementShape4 and break selection loop if element is preselected
// 2016-02-24 2016.0.126.4 implemented CmdMepElementShape.GetProfileTypes returing all duct connector shapes
// 2016-02-24 2016.0.126.5 updated readme and added keywords to all modules to improve global internet search results
// 2016-03-16 2016.0.126.6 implemented SetFamilyParameterValue sample code
// 2016-03-22 2016.0.126.7 implemented GetBeamsIntersectingTwoColumns
// 2016-04-05 2016.0.126.8 implemented DistinguishRooms
// 2016-04-06 2016.0.126.8 updated DistinguishRooms
// 2016-04-08 2016.0.126.9 renamed GetCorners to GetBottomCorners
// 2016-04-11 2016.0.126.10 implemeneted JtNamedGuiStorage skeleton
// 2016-04-11 2016.0.126.10 fleshed out the JtNamedGuiStorage class
// 2016-04-11 2016.0.127.0 implemented CmdNamedGuidStorage to test JtNamedGuiStorage
// 2016-04-12 2016.0.127.1 fixed typo in JtNamedGuidStorage
// 2016-04-12 2016.0.127.3 added Scott Wilson's reference stable representation magic voodoo
// 2016-05-02 2017.0.127.0 flat migration to Revit 2017 and first successful test run
// 2016-05-02 2017.0.127.1 eliminated all use of automatic transaction mode, untested!
// 2016-05-03 2017.0.127.2 eliminated use of obsolete Plane construction methods taking two XYZ arguments for normal and origin
// 2016-05-03 2017.0.127.3 eliminated two calls to obsolete Plane construction method taking a CurveArray argument
// 2016-05-03 2017.0.127.4 eliminated all obsolete Revit API usage warnings
// 2016-06-13 2017.0.127.5 implemented CreatePointLoadOnColumnEnd
// 2016-07-05 2017.0.127.6 implemented BoundingBoxXYZ ExpandToContain extension methods and GetModelExtents
// 2016-07-07 2017.0.127.7 implemented and tested ExportToImage3
// 2016-08-02 2017.0.127.8 implemented and tested GetBoundingBox for room boundary IList of IList of BoundarySegment
// 2016-08-15 2017.0.127.8 implemented SetSectionBox
// 2016-08-16 2017.0.127.9 implemented ConvexHull, GetConvexHullOfRoomBoundary, improved PointArrayString
// 2016-08-16 2017.0.127.10 call Distinct to eliminate duplicate points before calling ConvexHull
// 2016-08-24 2017.0.127.11 implemented SelectAndPlaceTakeOffFitting
// 2016-08-29 2017.0.128.0 implemented CmdPurgeLineStyles
// 2016-08-30 2017.0.128.1 refactored CmdPurgeLineStyles for simple migration to Revit macro
// 2016-09-13 2017.0.129.0 implemented CmdDeleteMacros
// 2016-09-27 2017.0.130.0 implemented CmdSetTangentLock
// 2016-09-29 2017.0.130.1 added general warning swallower
// 2016-09-30 2017.0.130.2 added CreateSolidFromBoundingBox
// 2016-10-06 2017.0.130.3 added testTwo macro to isolate element in new view
// 2016-10-07 2017.0.130.4 added material asset texture listing sample code
// 2016-10-25 2017.0.131.0 added CmdCreateLineStyle written by Scott Conover
// 2016-10-31 2017.0.131.1 added GetColumHeightFromLevels and GetElementHeightFromBoundingBox
// 2016-11-15 2017.0.131.2 moved GetElementLocation into Util class
// 2016-11-15 2017.0.131.2 added and commented out code to convert List<Element> to List<XYZ>
// 2016-12-07 2017.0.131.3 added Eriks View IntersectsBoundingBox extension method
// 2016-12-10 2017.0.131.4 added Joshuas ViewportBringToFront method
// 2016-12-24 2017.0.131.5 implemented JtElementIdExtensionMethods
// 2017-01-03 2017.0.131.6 incremented copyright year
// 2017-01-04 2017.0.131.7 integrated ViewportBringToFront enhancement suggested by akseidel@github
// 2017-01-17 2017.0.131.8 added CreateVerticalDimensioning
// 2017-01-22 2017.0.132.0 added Alexander Ignatovich' CmdSharedParamGuids
// 2017-01-24 2017.0.132.1 added SelectAllPhysicalElements and Element.IsPhysicalElement extension method
// 2017-01-24 2017.0.132.2 added WhereElementIsViewIndependent
// 2017-01-24 2017.0.132.3 added SetTextAlignment
// 2017-01-26 2017.0.132.4 implemented GetFamiliesOfCategory and FamilyFirstSymbolCategoryEquals
// 2017-02-02 2017.0.132.5 implemented JtLineExtensionMethods.Contains
// 2017-02-06 2017.0.132.6 correction to Line.Contains extension method suggested by Fair59 in http://forums.autodesk.com/t5/revit-api-forum/how-to-determine-if-a-point-xyz-is-inside-a-curveloop-ilist-lt/m-p/6856497
// 2017-02-09 2017.0.132.7 merged so-chong fix to typo in line style name pull request #3
// 2017-03-10 2017.0.132.8 implemented GetRoomsOnLevel for https://forums.autodesk.com/t5/revit-api-forum/collect-all-room-in-leve-xx/m-p/6936959
// 2017-03-14 2017.0.132.9 added GetFamilyInstanceLocation from https://forums.autodesk.com/t5/revit-api-forum/retrieve-family-instance-position/m-p/6943376
// 2017-03-17 2017.0.132.10 implemented GetAreasInAreaScheme for https://forums.autodesk.com/t5/revit-api-forum/get-area-scheme-from-an-area/m-p/6949212
// 2017-03-22 2017.0.132.11 cleaned up CmdCreateGableWall for http://thebuildingcoder.typepad.com/blog/2011/07/create-gable-wall.html#comment-3216411810
// 2017-03-22 2017.0.132.12 cleaned up JtRevision to avoid using parameter display names
// 2017-03-23 2017.0.132.13 implemented FootToMetre
// 2017-04-21 2018.0.132.0 flat migration to Revit 2018 and fixed initial compilation errors; 7 deprecation warnings remain
// 2017-04-21 2018.0.132.1 fixed some deprecation warnings; 3 deprecation warnings remain
// 2017-05-11 2018.0.132.2 catch OperationCanceledException when calling PromptForFamilyInstancePlacement
// 2017-05-17 2018.0.132.3 added IsElementVisibleInView from http://stackoverflow.com/questions/44012630/determine-is-a-familyinstance-is-visible-in-a-view
// 2017-05-22 2018.0.132.4 implemented CreateCone for https://forums.autodesk.com/t5/revit-api-forum/revolvedgeometry/m-p/7098852
// 2017-05-23 2018.0.132.5 implemented arbitrary axis algorithm in GetArbitraryAxes
// 2017-05-23 2018.0.132.5 rewrote CreateCone to take arbitrary base point and axis
// 2017-05-30 2018.0.133.0 implemented CmdSetGridEndpoint
// 2017-06-13 2018.0.133.1 added AlignOffAxisGrid from https://forums.autodesk.com/t5/revit-api-forum/grids-off-axis/m-p/7129065
// 2017-06-14 2018.0.134.0 implemented CmdGetDimensionPoints for https://forums.autodesk.com/t5/revit-api-forum/how-to-retrieve-a-dimension-s-segment-geometry/m-p/7145688
// 2017-06-23 2018.0.134.1 implemented ConnectorXyzComparer and ToHashSet extension method for https://forums.autodesk.com/t5/revit-api-forum/distinct-xyz/m-p/7173069
// 2017-08-15 2018.0.134.2 implemented GetFamilyInstancesByFamilyAndType and GetTitleBlockSymbolByFamilyAndType methods for https://forums.autodesk.com/t5/revit-api-forum/family-instance-filter/m-p/7287113
// 2017-08-24 2018.0.134.3 implemented OuterLoop and PlanarFaceOuterLoop methods for https://forums.autodesk.com/t5/revit-api-forum/is-the-first-edgeloop-still-the-outer-loop/m-p/7225379
// 2017-10-16 2018.0.134.4 added GetPlanarFaceOuterLoops from https://forums.autodesk.com/t5/revit-api-forum/outer-loops-of-planar-face-with-separate-parts/m-p/7461348
// 2017-10-22 2018.0.134.5 added FindTextureBitmapPaths for https://forums.autodesk.com/t5/revit-api-forum/extract-object-texture-information-using-api/m-p/7406055
// 2017-10-25 2018.0.134.6 added GetCurtainWallPanelGeometry
// 2017-10-25 2018.0.134.7 replace deprecated method NewTag by IndependentTag.Create
// 2017-10-25 2018.0.134.8 implemented Util.DoubleArrayString and replaced calls to deprecated property AssetPropertyDoubleArray3d.Value
// 2017-11-30 2018.0.134.9 added CreateWallsAutomaticallyCommand for https://forums.autodesk.com/t5/revit-api-forum/mathematical-translations/m-p/7580510
// 2017-12-05 2018.0.134.10 added CreateFaceWallsAndMassFloors for case 13663566 [APIによるマス床の生成方法 -- How to generate mass floor using API]
// 2017-12-20 2018.0.134.11 implemented Util.IsCollinear
// 2017-12-20 2018.0.134.11 added Miro's SetInstanceParamVaryBetweenGroupsBehaviour
// 2018-01-05 2018.0.134.12 incremented copyright year to 2018
// 2018-01-05 2018.0.134.13 implemented comparison operator for lines in the XY plane
// 2018-01-17 2018.0.134.14 added CalculateMatrixForGlobalToLocalCoordinateSystem
// 2018-01-31 2018.0.135.0 added CmdFailureGatherer.cs from https://forums.autodesk.com/t5/revit-api-forum/return-failure-information-to-command/m-p/7695676
// 2018-02-01 2018.0.135.2 added GetCropBoxFor
// 2018-02-06 2018.0.136.0 implemented CmdBrepBuilder
// 2018-02-07 2018.0.136.1 added RevitLinkType LoadFrom sample code
// 2018-02-12 2018.0.136.2 implemented ConvertLoopToArray for https://forums.autodesk.com/t5/revit-api-forum/fillet-and-curve-loop/m-p/7769993
// 2018-02-22 2018.0.136.3 added GetRevitTextColorFromSystemColor from https://forums.autodesk.com/t5/revit-api-forum/how-to-change-text-color/td-p/2567672
// 2018-02-22 2018.0.136.4 flipped plus to minus in ProjectOnto according to comment http://thebuildingcoder.typepad.com/blog/2014/09/planes-projections-and-picking-points.html#comment-3765750464
// 2018-02-24 2018.0.136.5 implemented set text note colour
// 2018-02-27 2018.0.136.6 tested and fixed ToColorParameterValue
// 2018-03-01 2018.0.136.7 added MepSystemSearch from https://github.com/geoffoverfield/RevitAPI_SystemSearch for https://forums.autodesk.com/t5/revit-api-forum/connector-neighbours/m-p/7816952
// 2018-03-04 2018.0.137.0 implemented CmdIntersectJunctionBox
// 2018-03-05 2018.0.137.0 updated CmdIntersectJunctionBox
// 2018-03-06 2018.0.137.1 implemented CreateArc2dFromRadiusStartAndEndPoint
// 2018-03-06 2018.0.137.2 added clockwise option to CreateArc2dFromRadiusStartAndEndPoint
// 2018-03-07 2018.0.138.0 implemented CmdSwitchDoc based on https://forums.autodesk.com/t5/revit-api-forum/change-active-document/m-p/7787792
// 2018-03-19 2018.0.138.1 added GetIntersectedSolidArea test code from https://forums.autodesk.com/t5/revit-api-forum/linked-file-element-intersection-solid-geometry/m-p/7861611
// 2018-03-21 2018.0.138.2 added GetRoomCenter from https://forums.autodesk.com/t5/revit-api-forum/create-roomtag/m-p/7871671
// 2018-04-05 2018.0.138.3 implemented RetrieveEdges for https://stackoverflow.com/questions/49651399/revit-api-filtering-elements-by-edges
// 2018-04-05 2018.0.138.4 added GetFamilyXmlData by Håvard Dagsvik
// 2018-04-18 2019.0.138.0 flat migration to Revit 2019; 6 deprecated API usage warnings about AssetProperties[] operator
// 2018-05-14 2019.0.138.2 implemented GetAllExteriorWalls for https://forums.autodesk.com/t5/revit-api-forum/how-do-i-get-all-the-outermost-walls-in-the-model/m-p/7998948 
// 2018-05-15 2019.0.139.0 implemented CmdProcessVisibleDwg for https://forums.autodesk.com/t5/revit-api-forum/visibility-of-dwg-layer/m-p/7975284
// 2018-05-15 2019.0.139.1 implemented NumberStructuralFraming for https://forums.autodesk.com/t5/revit-api-forum/set-different-value-to-a-set-of-elements/td-p/8004141
// 2018-05-16 2019.0.139.2 added missing commit
// 2018-05-17 2019.0.140.0 implemented CmdParamValuesForCats
// 2018-05-23 2019.0.141.0 implemented CmdExteriorWalls for https://forums.autodesk.com/t5/revit-api-forum/how-do-i-get-all-the-outermost-walls-in-the-model/m-p/7998948
// 2018-05-24 2019.0.141.1 added GetFamilyInstancesSatisfyingFilterRule from https://forums.autodesk.com/t5/revit-api-forum/how-to-filter-element-which-satisfy-filter-rule/m-p/8020317
// 2018-05-24 2019.0.142.0 added CmdFlowMismatch from https://forums.autodesk.com/t5/revit-api-forum/application-level-macro-flow-mismatch/m-p/8032555
// 2018-06-21 2019.0.142.1 added TestIntersect from https://forums.autodesk.com/t5/revit-api-forum/surprising-results-from-face-intersect-face-method/m-p/8079881
// 2018-07-10 2019.0.143.0 implemented CmdExportIfc for https://forums.autodesk.com/t5/revit-api-forum/ifc-export-using-document-export-not-working/m-p/8118082
// 2018-08-06 2019.0.143.1 fixed CmdWallProfile for https://forums.autodesk.com/t5/revit-api-forum/get-wall-profile-error-cmdwallprofile-cs/m-p/8178951
// 2018-08-26 2019.0.143.2 added DeleteNonSharedProjectParam for https://forums.autodesk.com/t5/revit-api-forum/deleting-a-non-shared-project-parameter/td-p/5975020
// 2018-08-26 2019.0.143.3 use LINQ Where clause in DeleteNonSharedProjectParam
// 2018-08-27 2019.0.143.4 tested CmdNewExtrusionRoof for https://forums.autodesk.com/t5/revit-api-forum/roof-by-extrusion/m-p/8220705#M32966
// 2018-08-28 2019.0.143.5 added GetCeilingReferenceAbove from http://thebuildingcoder.typepad.com/blog/2010/01/findreferencesbydirection.html#comment-4055509541
// 2018-09-04 2019.0.143.6 added broken and working commands by Austin Sudtelgte to CmdDeleteUnusedRefPlanes.cs
// 2018-09-04 2019.0.143.7 added GetFamilyInstanceReferencePlaneLocation by Fair59 from https://forums.autodesk.com/t5/revit-api-forum/direction-of-reference-reference-plane-or-reference-line/m-p/7074163
// 2018-09-14 2019.0.143.8 added GetGridRef and GetGenericFamilySymbolsNamedTest
// 2018-09-17 2019.0.143.9 optimised GetGenericFamilySymbolsNamedTest for https://forums.autodesk.com/t5/revit-api-forum/parameter-filter/m-p/8270495
// 2018-10-29 2019.0.143.10 use UiApplication MainWindowHandle to address issue #8, removed use of JtWindowHandle
// 2018-11-12 2019.0.144.0 implemented CmdMultistoryStairSubelements
// 2018-11-15 2019.0.144.1 compare element category to target category list for https://forums.autodesk.com/t5/revit-api-forum/implementing-iselection-interface-for-seclecting-some-specific/m-p/8403097
// 2018-11-28 2019.0.144.2 added code for dimensioning wall corners https://forums.autodesk.com/t5/revit-api-forum/dimension-between-walls-corners-using-revit-s-api/m-p/7228752
// 2018-12-03 2019.0.144.3 added DimensionBetweenDetaiLines for 14840395 [Revit APIでの寸法作成時の参照設定]
// 2018-12-06 2019.0.144.4 added GetIntersectingLinkedElementIds for https://forums.autodesk.com/t5/revit-api-forum/how-to-use-the-elementintersectselementfilter-from-the/m-p/8442649
// 2018-12-06 2019.0.144.5 implemented CompareCategoryToTargetList
// 2018-12-25 2019.0.144.6 implemented GetLargestHorizontalFace
// 2018-12-25 2019.0.144.6 implemented MedianPoint, TriangleArea and PointOnFace2
// 2018-12-28 2019.0.144.7 worked on CmdListAllRooms, handle empty boundary curve in GetConvexHullOfRoomBoundary
// 2018-12-31 2019.0.144.8 worked on CmdListAllRooms, added _exportBoundary and _exportCsv switches
// 2018-12-31 2019.0.144.8 implemented BoundingBoxString overload with allowNull argument
// 2018-12-31 2019.0.144.8 implemented GetBoundaryPoints and AddNewPoints
// 2019-01-01 2019.0.144.8 added _room_boundary_tolerance
// 2019-01-01 2019.0.144.8 added tolerance argument to IsEqual
// 2019-01-01 2019.0.144.8 added warning message about skipping all but first room boundary loop
// 2019-01-01 2019.0.144.8 added support for zero boundary loops in GetBoundaryPoints
// 2019-01-01 2019.0.144.8 log boundary points and assert horizontal boundary
// 2019-01-01 2019.0.144.8 cleaned up logging of undefined lower left corner
// 2019-01-02 2019.0.144.8 add support fo empty list in AddNewPoints, test and cleanup
// 2019-01-02 2019.0.144.9 implemented CSV export for CmdListAllRooms
// 2019-01-02 2019.0.144.10 implemented PointArrayString for UV points
// 2019-01-02 2019.0.144.10 remove Z component from room boundary and convex hull
// 2019-01-02 2019.0.144.10 add support for IEnumerable when converting list to string
// 2019-01-03 2019.0.144.11 use spaces only for point array separator
// 2019-01-03 2019.0.144.11 implemented onlySpaceSeparator argument for PointString and PointArrayString
// 2019-01-03 2019.0.144.12 implemented IntPoint2d
// 2019-01-03 2019.0.144.12 implemented onlySpaceSeparator for IntPoint2d
// 2019-01-03 2019.0.144.13 implemented IntPoint3d
// 2019-01-03 2019.0.144.14 export room boundaries in millimetres
// 2019-01-09 2019.0.144.15 update copyright year to 2019
// 2019-01-10 2019.0.145.0 implemented CmdDuctResize for https://forums.autodesk.com/t5/revit-api-forum/find-all-ducts-that-have-been-tapped-into/m-p/8485269
// 2019-01-10 2019.0.145.0 fixed compilation error
// 2019-01-10 2019.0.145.0 replaced DuctResize with second version by jared in https://forums.autodesk.com/t5/revit-api-forum/find-all-ducts-that-have-been-tapped-into/m-p/8485269
// 2019-01-10 2019.0.145.1 replace DuctResize by second version from Jared
// 2019-01-10 2019.0.145.2 check for null instead of exception, no rollback required, ask only if needed
// 2019-01-10 2019.0.145.3 only set updated height if it differs from old, show results dialogue when nothing was changed, use GetElementCount and only count really modified ducts, successfully tested
// 2019-01-10 2019.0.145.4 rebuilt duct size retrieval logic from scratch and eliminated catch-all exception handler
// 2019-01-14 2019.0.145.5 implemented GetDuctShape
// 2019-01-17 2019.0.145.6 implemented GetCountPerTypePerCategory for https://forums.autodesk.com/t5/revit-api-forum/alternate-to-slow-filter/td-p/8528704
// 2019-02-04 2019.0.145.7 implemented GetWallMepClashes for https://forums.autodesk.com/t5/revit-api-forum/aborting-long-running-elementintersectselementfilter/m-p/8566911
// 2019-02-14 2019.0.145.8 added CreateSweepWithMultipleLoops from https://forums.autodesk.com/t5/revit-api-forum/how-to-create-a-sweep-with-multiple-closed-loops-in-profile/m-p/8477617 
// 2019-02-26 2019.0.145.9 added GetPipesForSystemType from https://forums.autodesk.com/t5/revit-api-forum/filteredelementcollector-by-pipe-system-types/m-p/8620113
// 2019-02-26 2019.0.145.10 implemented GetSpecificTitleBlockType for https://forums.autodesk.com/t5/revit-api-forum/insert-specific-title-block/m-p/8621988
// 2019-03-02 2019.0.145.11 eliminated all deprecated API calls to achieve zero compilation warnings
// 2019-03-08 2019.0.145.12 implemented CreateCurveLoop and OffsetPoints for https://forums.autodesk.com/t5/revit-api-forum/offset-xyz-points/m-p/8665334
// 2019-03-27 2019.0.145.13 implemented bounding box Clear, ExpandToContain enum of points and GetBoundingBox for CurveLoop for https://forums.autodesk.com/t5/revit-api-forum/how-to-get-width-and-height-of-curveloop/m-p/8686230
// 2019-04-03 2019.0.145.14 implemented GetInstancesOfElementType for https://forums.autodesk.com/t5/revit-api-forum/get-all-instances-of-given-elementtype/m-p/8703667
// 2019-04-03 2019.0.145.15 Sudhan corrected GetFamilyInstancesByFamilyAndType
// 2019-04-07 2019.0.145.16 cleaned up samples demonstrating retrieving named family symbols using either LINQ or a parameter filter
// 2019-04-08 2019.0.145.17 implemented SetFloorLevelAndOffset for https://forums.autodesk.com/t5/revit-api-forum/changing-the-level-id-and-offset-height-of-floors/m-p/8714247
// 2019-04-24 2020.0.145.0 flat migration to Revit 2020
// 2019-04-24 2020.0.145.1 implemented CloseDocByCommand suggested by Bogdan
// 2019-05-02 2020.0.145.2 implemented GetElementTypeByName, GetFamilySymbolByName and GetTextNoteTypeByName
// 2019-05-02 2020.0.145.3 implemented DeleteNonRoomSeparators for https://forums.autodesk.com/t5/revit-api-forum/deleting-lines-that-are-not-assigned-to-the-lt-room-separation/m-p/8765491
// 2019-05-02 2020.0.145.4 renamed BeamCreator and cleanup
// 2019-05-13 2020.0.145.5 added TagAllLinkedWalls from https://forums.autodesk.com/t5/revit-api-forum/tagging-linked-elements-using-revit-api/m-p/8787094
// 2019-05-14 2020.0.145.6 implemented CreateCylinder for https://forums.autodesk.com/t5/revit-api-forum/how-to-find-one-element-inside-other-element/m-p/8789016
// 2019-06-03 2020.0.146.0 implemented CmdBim360Links
// 2019-06-19 2020.0.146.1 implemented ListElementsInAssembly for https://forums.autodesk.com/t5/revit-api-forum/get-list-of-elements-in-assembly/m-p/8857972
// 2019-06-20 2020.0.146.2 implemented CreatePerspectiveViewMatchingCamera
// 2019-06-21 2020.0.147.0 implemented CmdRebarCurves
// 2019-06-21 2020.0.147.1 added summary report to CmdRebarCurves
// 2019-07-22 2020.0.147.1 implemented GetLightSourceGraphicsStyleElementId
// 2019-08-04 2020.0.147.2 added Intersect from https://github.com/ArashPartow/wykobi
// 2019-08-05 2020.0.147.3 implemented PullTextFromAnnotationTags for case 15623936
// 2019-08-05 2020.0.147.4 added code by Alexander and Jorge to dimension filled regions from https://forums.autodesk.com/t5/revit-api-forum/create-dimensions-for-filled-region-boundary/m-p/8926301
// 2019-08-27 2020.0.147.5 cleaned up and added input argumnets to CreatePerspectiveViewMatchingCamera
// 2019-09-02 2020.0.147.6 implemented ReadTitleBlockLabelParameters for 15711698 [Get Label Parameters]
// 2019-09-04 2020.0.147.7 added GetDoorSymbolsForCurtainWall from https://forums.autodesk.com/t5/revit-api-forum/builtincategory-of-doors-and-curtain-wall-doors/m-p/9002988
// 
[assembly: AssemblyVersion( "2020.0.147.7" )]
[assembly: AssemblyFileVersion( "2020.0.147.7" )]
