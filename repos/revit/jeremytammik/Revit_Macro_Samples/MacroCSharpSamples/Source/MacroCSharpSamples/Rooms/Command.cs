//
// (C) Copyright 2003-2007 by Autodesk, Inc.
//
// Permission to use, copy, modify, and distribute this software in
// object code form for any purpose and without fee is hereby granted,
// provided that the above copyright notice appears in all copies and
// that both that copyright notice and the limited warranty and
// restricted rights notice below appear in all supporting
// documentation.
//
// AUTODESK PROVIDES THIS PROGRAM "AS IS" AND WITH ALL FAULTS.
// AUTODESK SPECIFICALLY DISCLAIMS ANY IMPLIED WARRANTY OF
// MERCHANTABILITY OR FITNESS FOR A PARTICULAR USE. AUTODESK, INC.
// DOES NOT WARRANT THAT THE OPERATION OF THE PROGRAM WILL BE
// UNINTERRUPTED OR ERROR FREE.
//
// Use, duplication, or disclosure by the U.S. Government is subject to
// restrictions set forth in FAR 52.227-19 (Commercial Computer
// Software - Restricted Rights) and DFAR 252.227-7013(c)(1)(ii)
// (Rights in Technical Data and Computer Software), as applicable.
//


using System;
using System.Windows.Forms;

using Autodesk.Revit;
using Autodesk.Revit.DB;
using Autodesk.Revit.DB.Structure;

using MacroCSharpSamples;

namespace Revit.SDK.Samples.Rooms.CS
{
	/// <summary>
	/// Get some properties of a slab , such as Level, Type name, Span direction,
	/// Material name, Thickness, and Young Modulus for the slab's Material.
	/// </summary>
    public class SamplesRoom
    {
 //       #region Class ctor implemetation
        /// <summary>
        /// Ctor without parameter is not allowed
        /// </summary>
        private SamplesRoom()
        {
            // no codes
        }

        /// <summary>
        /// Default constructor of StructuralLayerFunction
        /// </summary>
        public SamplesRoom(ThisDocument hostDoc)
        {
            // Init for varialbes
            // this document handler
            m_doc = hostDoc;
        }

        /// <summary>
        /// Run sample Rooms
        /// </summary>
        public void Run()
        {
            try
            {
                //create a new instance of class Data
                RoomsData data = new RoomsData(m_doc, m_doc.Document.Application);
                //create a form to display the room information
                using (roomsInformationForm infoForm = new roomsInformationForm(data))
                {
                    infoForm.ShowDialog();
                }
            }
            catch (Exception ex)
            {
                // If there are something wrong, give error information
                MessageBox.Show(ex.Message);
            }
        }

        #region Class member variable
        ThisDocument m_doc;
        #endregion 
    }
}
