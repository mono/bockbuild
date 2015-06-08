GitHubPackage('mono', 'gtk-sharp', '2-12-branch',
              revision='2c30524200ccd1a4913204fc1cbbd925084d386b',
              override_properties={'configure':
                                   './bootstrap-2.12 --prefix="%{prefix}"'
                                   })
