﻿//------------------------------------------------------------------------------
// <auto-generated>
//     This code was generated by a tool.
//     Runtime Version:4.0.30319.42000
//
//     Changes to this file may cause incorrect behavior and will be lost if
//     the code is regenerated.
// </auto-generated>
//------------------------------------------------------------------------------

namespace REX.Unit.Resources.Strings {
    using System;
    
    
    /// <summary>
    ///   A strongly-typed resource class, for looking up localized strings, etc.
    /// </summary>
    // This class was auto-generated by the StronglyTypedResourceBuilder
    // class via a tool like ResGen or Visual Studio.
    // To add or remove a member, edit your .ResX file then rerun ResGen
    // with the /str option, or rebuild your VS project.
    [global::System.CodeDom.Compiler.GeneratedCodeAttribute("System.Resources.Tools.StronglyTypedResourceBuilder", "4.0.0.0")]
    [global::System.Diagnostics.DebuggerNonUserCodeAttribute()]
    [global::System.Runtime.CompilerServices.CompilerGeneratedAttribute()]
    internal class Texts {
        
        private static global::System.Resources.ResourceManager resourceMan;
        
        private static global::System.Globalization.CultureInfo resourceCulture;
        
        [global::System.Diagnostics.CodeAnalysis.SuppressMessageAttribute("Microsoft.Performance", "CA1811:AvoidUncalledPrivateCode")]
        internal Texts() {
        }
        
        /// <summary>
        ///   Returns the cached ResourceManager instance used by this class.
        /// </summary>
        [global::System.ComponentModel.EditorBrowsableAttribute(global::System.ComponentModel.EditorBrowsableState.Advanced)]
        internal static global::System.Resources.ResourceManager ResourceManager {
            get {
                if (object.ReferenceEquals(resourceMan, null)) {
                    global::System.Resources.ResourceManager temp = new global::System.Resources.ResourceManager("REX.Unit.Resources.Strings.Texts", typeof(Texts).Assembly);
                    resourceMan = temp;
                }
                return resourceMan;
            }
        }
        
        /// <summary>
        ///   Overrides the current thread's CurrentUICulture property for all
        ///   resource lookups using this strongly typed resource class.
        /// </summary>
        [global::System.ComponentModel.EditorBrowsableAttribute(global::System.ComponentModel.EditorBrowsableState.Advanced)]
        internal static global::System.Globalization.CultureInfo Culture {
            get {
                return resourceCulture;
            }
            set {
                resourceCulture = value;
            }
        }
        
        /// <summary>
        ///   Looks up a localized string similar to Data.
        /// </summary>
        internal static string LIST_Data {
            get {
                return ResourceManager.GetString("LIST_Data", resourceCulture);
            }
        }
        
        /// <summary>
        ///   Looks up a localized string similar to Results.
        /// </summary>
        internal static string LIST_Results {
            get {
                return ResourceManager.GetString("LIST_Results", resourceCulture);
            }
        }
        
        /// <summary>
        ///   Looks up a localized string similar to Question.
        /// </summary>
        internal static string MessageBox_CaptionQuestion {
            get {
                return ResourceManager.GetString("MessageBox_CaptionQuestion", resourceCulture);
            }
        }
        
        /// <summary>
        ///   Looks up a localized string similar to Errors occurred! Do you want to continue?.
        /// </summary>
        internal static string MessageBox_ErrorQuestion {
            get {
                return ResourceManager.GetString("MessageBox_ErrorQuestion", resourceCulture);
            }
        }
        
        /// <summary>
        ///   Looks up a localized string similar to Unit.
        /// </summary>
        internal static string REX_ModuleDescription {
            get {
                return ResourceManager.GetString("REX_ModuleDescription", resourceCulture);
            }
        }
        
        /// <summary>
        ///   Looks up a localized string similar to To launch this extension, Extensions Engine at least version %vern should be installed.\nThe current version is: %verc.
        /// </summary>
        internal static string REX_VersionInfo {
            get {
                return ResourceManager.GetString("REX_VersionInfo", resourceCulture);
            }
        }
    }
}
