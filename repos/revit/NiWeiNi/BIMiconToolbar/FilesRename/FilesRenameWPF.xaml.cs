﻿using System;
using System.Collections.ObjectModel;
using System.ComponentModel;
using System.Text.RegularExpressions;
using System.Windows;
using System.Windows.Controls;

namespace BIMiconToolbar.FilesRename
{
    /// <summary>
    /// Interaction logic for FilesRenameWPF.xaml
    /// </summary>
    public partial class FilesRenameWPF : Window, IDisposable, INotifyPropertyChanged
    {
        public event PropertyChangedEventHandler PropertyChanged;

        // Variables to hold user input
        public bool filesRenameBool = true;
        public bool Canceled = true;
        public string SelectedPath { get; set; }

        public ObservableCollection<ComboBoxItem> CbFileType{ get; set; }
        public ComboBoxItem SelectedComboItemFileType { get; set; }

        public string NamePrefix { get; set; }
        public string NameSuffix { get; set; }

        public string NameFind { get; set; }
        public string NameReplace { get; set; }

        private string nameDestinationPath;
        public string NameDestinationPath
        {
            get { return nameDestinationPath; }
            set
            {
                if (value != nameDestinationPath)
                {
                    nameDestinationPath = value;
                    OnPropertyChanged("NameDestinationPath");
                }
            }
        }

        /// <summary>
        /// Main function to call window
        /// </summary>
        public FilesRenameWPF(string selectedPath)
        {
            InitializeComponent();
            DataContext = this;

            // Set path to display as selectedPath
            this.currentPath.Text = selectedPath;
            SelectedPath = selectedPath;

            // Populate comboBox
            FileTypes(selectedPath);

            NameDestinationPath = SelectedPath;
        }

        /// <summary>
        /// 
        /// </summary>
        /// <param name="propertyName"></param>
        protected void OnPropertyChanged(string propertyName)
        {
            PropertyChangedEventHandler handler = PropertyChanged;
            if (handler != null)
            {
                handler(this, new PropertyChangedEventArgs(propertyName));
            }
        }

        /// <summary>
        /// Function to close window
        /// </summary>
        public void Dispose()
        {
            this.Close();
        }

        /// <summary>
        /// Functon to toggle file or folder selection
        /// </summary>
        /// <param name="sender"></param>
        /// <param name="e"></param>
        private void FoldersRename_Checked(object sender, RoutedEventArgs e)
        {
            this.filesRenameBool = !filesRenameBool;

            // Toggle enable/dissable dropdown list of file types
            this.comboDisplayFileType.IsEnabled = !this.comboDisplayFileType.IsEnabled;

            // Switch between display file or folder rename
            NameDestinationPath = Helpers.HelpersDirectory.UpdatePathName(filesRenameBool,
                                                                          SelectedComboItemFileType,
                                                                          SelectedPath,
                                                                          NameFind,
                                                                          NameReplace,
                                                                          NamePrefix,
                                                                          NameSuffix);
        }

        /// <summary>
        /// Function to retrieve file types
        /// </summary>
        /// <param name="selectedPath"></param>
        public void FileTypes(string selectedPath)
        {
            CbFileType = new ObservableCollection<ComboBoxItem>();

            var files = Helpers.HelpersDirectory.RetrieveFiles(selectedPath);

            var fileTypes = Helpers.HelpersDirectory.GetFilesType(files);

            // Populate the comboBoxes
            bool populateFirst = true;

            foreach (var ext in fileTypes)
            {
                ComboBoxItem comb = new ComboBoxItem();
                comb.Content = ext;
                CbFileType.Add(comb);

                // Set the first item to display in comboBox
                if (populateFirst)
                {
                    SelectedComboItemFileType = comb;
                    populateFirst = false;
                }
            }
        }

        /// <summary>
        /// Function to confirm input in window
        /// </summary>
        /// <param name="sender"></param>
        /// <param name="e"></param>
        private void OK_Click(object sender, RoutedEventArgs e)
        {
            string[] oldNames;

            // Retrieve all files names inside path
            if (filesRenameBool)
            {
                oldNames = Helpers.HelpersDirectory.GetFilesMatchPattern(SelectedPath, "*" + (string)SelectedComboItemFileType.Content);
            }
            // Retrieve all folder names inside path
            else
            {
                oldNames = Helpers.HelpersDirectory.GetDirectoriesFromPath(SelectedPath);
            }
            
            // Create new names for folders or files
            string[] newNames = Helpers.HelpersDirectory.CreateNewNames(oldNames, NamePrefix, NameSuffix, NameFind, NameReplace, filesRenameBool);

            // Rename files
            if (filesRenameBool)
            {
                Helpers.HelpersDirectory.RenameFiles(oldNames, newNames);
            }
            // Move folders and rename
            else
            {
                Helpers.HelpersDirectory.MoveDirectories(oldNames, newNames);
            }

            this.Dispose();
        }

        /// <summary>
        /// Function to close the current window
        /// </summary>
        /// <param name="sender"></param>
        /// <param name="e"></param>
        private void Cancel_Click(object sender, RoutedEventArgs e)
        {
            this.Dispose();
        }

        /// <summary>
        /// Function to update property namePrefix
        /// </summary>
        /// <param name="sender"></param>
        /// <param name="e"></param>
        private void PrefixTextBox_TextChanged(object sender, TextChangedEventArgs e)
        {
            NamePrefix = TextChanged(sender, e);
            NameDestinationPath = Helpers.HelpersDirectory.UpdatePathName(filesRenameBool,
                                                              SelectedComboItemFileType,
                                                              SelectedPath,
                                                              NameFind,
                                                              NameReplace,
                                                              NamePrefix,
                                                              NameSuffix);
        }

        /// <summary>
        /// Function to update nameSuffix
        /// </summary>
        /// <param name="sender"></param>
        /// <param name="e"></param>
        private void SuffixTextBox_TextChanged(object sender, TextChangedEventArgs e)
        {
            NameSuffix = TextChanged(sender, e);
            NameDestinationPath = Helpers.HelpersDirectory.UpdatePathName(filesRenameBool,
                                                              SelectedComboItemFileType,
                                                              SelectedPath,
                                                              NameFind,
                                                              NameReplace,
                                                              NamePrefix,
                                                              NameSuffix);
        }

        /// <summary>
        /// Function to change findText
        /// </summary>
        /// <param name="sender"></param>
        /// <param name="e"></param>
        private void FindText_TextChanged(object sender, TextChangedEventArgs e)
        {
            NameFind = TextChanged(sender, e);
            NameDestinationPath = Helpers.HelpersDirectory.UpdatePathName(filesRenameBool,
                                                              SelectedComboItemFileType,
                                                              SelectedPath,
                                                              NameFind,
                                                              NameReplace,
                                                              NamePrefix,
                                                              NameSuffix);
        }

        /// <summary>
        /// Function to change replaceText
        /// </summary>
        /// <param name="sender"></param>
        /// <param name="e"></param>
        private void ReplaceText_TextChanged(object sender, TextChangedEventArgs e)
        {
            NameReplace = TextChanged(sender, e);
            NameDestinationPath = Helpers.HelpersDirectory.UpdatePathName(filesRenameBool,
                                                              SelectedComboItemFileType,
                                                              SelectedPath,
                                                              NameFind,
                                                              NameReplace,
                                                              NamePrefix,
                                                              NameSuffix);
        }

        /// <summary>
        /// Function to update TextBoxes
        /// </summary>
        /// <param name="sender"></param>
        /// <param name="e"></param>
        private string TextChanged(object sender, TextChangedEventArgs e)
        {
            // Store the content of the textbox
            string stringCheck = (sender as TextBox).Text;

            return Helpers.Parsing.RemoveForbiddenChars(stringCheck);
        }

        /// <summary>
        /// Function to remove placeholder text in textboxes
        /// </summary>
        /// <param name="sender"></param>
        /// <param name="e"></param>
        public void GotFocus(object sender, RoutedEventArgs e)
        {
            TextBox tb = (TextBox)sender;
            tb.Text = string.Empty;
            tb.GotFocus -= GotFocus;
        }

        /// <summary>
        /// Function to handle change in combobox
        /// </summary>
        /// <param name="sender"></param>
        /// <param name="e"></param>
        private void ComboDisplayFileType_SelectionChanged(object sender, SelectionChangedEventArgs e)
        {
            NameDestinationPath = Helpers.HelpersDirectory.UpdatePathName(filesRenameBool,
                                                              SelectedComboItemFileType,
                                                              SelectedPath,
                                                              NameFind,
                                                              NameReplace,
                                                              NamePrefix,
                                                              NameSuffix);
        }
    }
}
