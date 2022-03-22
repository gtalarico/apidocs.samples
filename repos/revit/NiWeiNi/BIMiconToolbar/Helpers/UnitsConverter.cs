﻿using Autodesk.Revit.DB;

namespace BIMiconToolbar.Helpers
{
    class UnitsConverter
    {
        /// <summary>
        /// Method to convert length units to Internal Units
        /// </summary>
        /// <param name="number"></param>
        /// <param name="dUT"></param>
        /// <returns></returns>
        public static double LengthUnitToInternal(double number, DisplayUnitType dUT)
        {
            return UnitUtils.ConvertToInternalUnits(number, dUT);
        }
    }
}
