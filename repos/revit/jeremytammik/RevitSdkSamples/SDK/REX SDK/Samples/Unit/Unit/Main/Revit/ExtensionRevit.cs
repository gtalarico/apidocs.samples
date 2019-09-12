//
// (C) Copyright 2007-2011 by Autodesk, Inc. All rights reserved.
//
// Permission to use, copy, modify, and distribute this software in
// object code form for any purpose and without fee is hereby granted
// provided that the above copyright notice appears in all copies and
// that both that copyright notice and the limited warranty and
// restricted rights notice below appear in all supporting
// documentation.
//
// AUTODESK PROVIDES THIS PROGRAM 'AS IS' AND WITH ALL ITS FAULTS.
// AUTODESK SPECIFICALLY DISCLAIMS ANY IMPLIED WARRANTY OF
// MERCHANTABILITY OR FITNESS FOR A PARTICULAR USE. AUTODESK, INC.
// DOES NOT WARRANT THAT THE OPERATION OF THE PROGRAM WILL BE
// UNINTERRUPTED OR ERROR FREE.
//
// Use, duplication, or disclosure by the U.S. Government is subject to
// restrictions set forth in FAR 52.227-19 (Commercial Computer
// Software - Restricted Rights) and DFAR 252.227-7013(c)(1)(ii)
// (Rights in Technical Data and Computer Software), as applicable.

using System;
using System.Collections.Generic;
using System.Text;

using Autodesk.REX.Framework;
using REX.Common;

namespace REX.Unit.Main.Revit
{
    internal class ExtensionRevit : REXExtensionProduct
    {
        public ExtensionRevit(REX.Common.REXExtension Ext)
            : base(Ext)
        {
        }

        /// <summary>
        /// Get the main extension.
        /// </summary>
        /// <value>The main extension.</value>
        internal Extension ThisMainExtension
        {
            get
            {
                return (Extension)ThisExtension;
            }
        }

        /// <summary>
        /// Get the Data structure.
        /// </summary>
        /// <value>The main Data.</value>
        internal Data ThisMainData
        {
            get
            {
                return ThisMainExtension.Data;
            }
        }

        #region REXExtensionProduct Members

        public override bool OnInitialize()
        {
            // insert code here.

            return true;
        }

        public override void OnCreate()
        {
            // insert code here.
        }

        public override void OnCreateDialogs()
        {
            // insert code here.
        }

        public override void OnCreateLayout()
        {
            // insert code here.
        }

        public override void OnSetDialogs()
        {
            // insert code here.
        }

        public override void OnSetData()
        {
            // insert code here.
        }

        public override void OnActivateLayout(REX.Common.REXLayoutItem LItem, bool Activate)
        {
            // insert code here.
        }

        public override bool OnCanRun()
        {
            // insert code here.

            return true;
        }

        public override void OnRun()
        {
            // insert code here.
        }

        public override bool OnCanClose()
        {
            // insert code here.

            return true;
        }

        public override bool OnCanClose(REX.Common.REXCanCloseType Type)
        {
            // insert code here.

            return true;
        }

        public override void OnClose()
        {
            // insert code here.
        }

        #endregion
    }
}
