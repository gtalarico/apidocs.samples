﻿using System;
using System.Collections.Generic;
using Rhino.Geometry;

namespace SampleGhPlatonics.Geometry
{
  public class Icosahedron : PlatonicGeometryBase
  {
    public override string DisplayName => "Icosahedron";

    public override int VertexCount => 12;

    public override int EdgeCount => 20;

    public override Point3d[] Vertices()
    {
      var c0 = (1.0 + Math.Sqrt(5.0)) / 4.0;

      var v = new List<Point3d>(VertexCount)
      {
        new Point3d(0.5, 0.0, c0),
        new Point3d(0.5, 0.0, -c0),
        new Point3d(-0.5, 0.0, c0),
        new Point3d(-0.5, 0.0, -c0),
        new Point3d(c0, 0.5, 0.0),
        new Point3d(c0, -0.5, 0.0),
        new Point3d(-c0, 0.5, 0.0),
        new Point3d(-c0, -0.5, 0.0),
        new Point3d(0.0, c0, 0.5),
        new Point3d(0.0, c0, -0.5),
        new Point3d(0.0, -c0, 0.5),
        new Point3d(0.0, -c0, -0.5)
      };
      return v.ToArray();
    }

    public override PolylineCurve[] Edges()
    {
      var v = Vertices();
      if (VertexCount != v.Length)
        return null;

      var e = new List<PolylineCurve>(EdgeCount)
      {
        CreateEdge(v[0], v[2], v[10]),
        CreateEdge(v[0], v[10], v[5]),
        CreateEdge(v[0], v[5], v[4]),
        CreateEdge(v[0], v[4], v[8]),
        CreateEdge(v[0], v[8], v[2]),
        CreateEdge(v[2], v[8], v[6]),
        CreateEdge(v[2], v[6], v[7]),
        CreateEdge(v[2], v[7], v[10]),
        CreateEdge(v[10], v[7], v[11]),
        CreateEdge(v[10], v[11], v[5]),
        CreateEdge(v[5], v[11], v[1]),
        CreateEdge(v[5], v[1], v[4]),
        CreateEdge(v[4], v[1], v[9]),
        CreateEdge(v[4], v[9], v[8]),
        CreateEdge(v[8], v[9], v[6]),
        CreateEdge(v[6], v[9], v[3]),
        CreateEdge(v[6], v[3], v[7]),
        CreateEdge(v[7], v[3], v[11]),
        CreateEdge(v[11], v[3], v[1]),
        CreateEdge(v[1], v[3], v[9])
      };
      return e.ToArray();
    }
  }
}
