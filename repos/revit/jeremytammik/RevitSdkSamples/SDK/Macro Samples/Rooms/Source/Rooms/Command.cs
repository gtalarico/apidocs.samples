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

namespace Rooms
{
	/// <summary>
	/// Get some properties of a slab , such as Level, Type name, Span direction,
	/// Material name, Thickness, and Young Modulus for the slab's Material.
	/// </summary>
    public class SamplesRoom
    {
        /// <summary>
        /// Ctor without parameter is not allowed
        /// </summary>
        private SamplesRoom()
        {
            // no code here
        }

        /// <summary>
        /// Default constructor of StructuralLayerFunction
        /// </summary>
        public SamplesRoom(ThisApplication hostApp)
        {
            // Init for varialbes
            // this application handler
            m_revit = hostApp;
        }

        /// <summary>
        /// Run sample Rooms
        /// </summary>
        public void Run()
        {
            if (null == m_revit.ActiveUIDocument)
            {
                MessageBox.Show("No openning document.");
                return;
            }

            Transaction trans = new Transaction(m_revit.ActiveUIDocument.Document, "RoomInfo");
            trans.Start();
            try
            {
                //create a new instance of class Data
                RoomsData data = new RoomsData(m_revit);
                //create a form to display the room information
                using (roomsInformationForm infoForm = new roomsInformationForm(data))
                {
                    infoForm.ShowDialog();
                }
            }
            catch (Exception ex)
            {
                // If there are something wrong, give error information
                trans.RollBack();
                MessageBox.Show(ex.Message);
            }
            trans.Commit();
        }

        #region Class member variable
        ThisApplication m_revit;
        #endregion 
    }
}
