﻿
/*
partial class Examples
{
  public static Rhino.Commands.Result Sweep2(Rhino.RhinoDoc doc)
  {
    // Select first rail curve
    Rhino.DocObjects.ObjRef rail1objref, rail2objref;
    var rc = Rhino.Input.RhinoGet.GetOneObject("Select first rail curve", false, Rhino.DocObjects.ObjectType.Curve, out rail1objref);
    if( rc!= Rhino.Commands.Result.Success)
      return rc;
    var rail1obj = rail1objref.Object();
    
    // Select second rail curve
    rc = Rhino.Input.RhinoGet.GetOneObject("Select second rail curve", false, Rhino.DocObjects.ObjectType.Curve, out rail2objref);
    if( rc!= Rhino.Commands.Result.Success)
      return rc;
    var rail2obj = rail2objref.Object();
  
    // Select cross section curves
    Rhino.DocObjects.ObjRef[] crosssecrefs;
    rc = Rhino.Input.RhinoGet.GetMultipleObjects("Select cross section curves", false, Rhino.DocObjects.ObjectType.Curve, out crosssecrefs);
    if( rc!= Rhino.Commands.Result.Success)
      return rc;

    Rhino.Geometry.Curve[] curves = new Rhino.Geometry.Curve[crosssecrefs.Length];
    for( int i=0; i<crosssecrefs.Length; i++ )
      curves[i] = crosssecrefs[i].Curve();
 
    // Call MySweep2 function
    Rhino.Geometry.Brep[] Sweep2_Breps = MySweep2(Rail1, Rail1_obj, Rail2, Rail2_obj, sCurves);
    if( Sweep2_Breps.Length>0  )
    {
      // Add to document
      for( int i=0; i<Sweep2_Breps.Length; i++ )
        doc.Objects.AddBrep(Sweep2_Breps[i]);

      doc.Views.Redraw();
    }
    return Rhino.Commands.Result.Success;
  }

  static Rhino.Geometry.Brep[] MySweep2( Rhino.Geometry.Curve rail1, Rhino.DocObjects.RhinoObject rail1object, Rhino.Geometry.Curve rail2, Rhino.DocObjects.RhinoObject rail2obj, Rhino.Geometry.Curve[] curves)
  {
    // Do some rail direction matching
    if (!Rhino.Geometry.Curve.DoDirectionsMatch(rail1, rail2))
      rail2.Reverse();

    Rhino.Geometry.SweepTwoRail sweep = new Rhino.Geometry.SweepTwoRail();

    // Define a new class that contains sweep2 arguments
  CArgsRhinoSweep2 args;
 
  // Set the 2 rails
  CRhinoPolyEdge Edge1, Edge2;
  Edge1.Create( Rail1, Rail1_obj );
  Edge2.Create( Rail2, Rail2_obj );
 
 
  // Add rails to sweep arguments
  args.m_rail_curves[0] = &Edge1;
  args.m_rail_curves[1] = &Edge2;
 
  args.m_rail_pick_points[0] = ON_UNSET_POINT;
  args.m_rail_pick_points[1] = ON_UNSET_POINT;
 
  // To create a closed sweep, you need to have:
  //  1. Two closed rail curves and and a single shape curve, or
  //  2. Set CArgsRhinoSweep2::m_bClosed = true
  args.m_bClosed = false;
 
  double tol = doc->AbsoluteTolerance();
 
  // Loop through sections to set parameters
  for( int i = 0; i < curves.Length; i++ )
  {
    var curve = curves[i];
 
    // Add to shapes
    args.m_shape_curves.Append( sCurve );
 
    // Cook up some rail parameters
    double t0 = 0.0;
    if( !GetShapeParameterOnRail(*sCurve, Edge1, tol, t0) )
      return false;
    args.m_rail_params[0].Append( t0 );
 
    double t1 = 0.0;
    if( !GetShapeParameterOnRail(*sCurve, Edge2, tol, t1) )
      return false;
    args.m_rail_params[1].Append( t1 );
  }
 
  // Set the rest of parameters
  args.m_simplify = 0;
  args.m_bSimpleSweep = false;
  args.m_bSameHeight = false;
  args.m_rebuild_count = -1; //Sample point count for rebuilding shapes
  args.m_refit_tolerance = tol;
  args.m_sweep_tolerance = tol;
  args.m_angle_tolerance = doc->AngleToleranceRadians();
 
  // Sweep2
  return RhinoSweep2(args, Sweep2_Breps) ? true : false;
}
 
}
*/