﻿using System;
using System.Collections.Generic;
using Rhino;
using Rhino.Commands;
using Rhino.Geometry;
using Rhino.Input;
using Rhino.Input.Custom;

namespace SampleCsSnapshotsClient
{
  public class SampleCsSnapshotsClientCommand : Command
  {
    public SampleCsSnapshotsClientCommand()
    {
      // Rhino only creates one instance of each command class defined in a
      // plug-in, so it is safe to store a refence in a static property.
      Instance = this;
    }

    ///<summary>The only instance of this command.</summary>
    public static SampleCsSnapshotsClientCommand Instance
    {
      get; private set;
    }

    ///<returns>The command name as it appears on the Rhino command line.</returns>
    public override string EnglishName
    {
      get { return "SampleCsSnapshotsClientCommand"; }
    }

    protected override Result RunCommand(RhinoDoc doc, RunMode mode)
    {
      RhinoApp.WriteLine("The {0} command is under construction.", EnglishName);

      return Result.Success;
    }
  }
}
