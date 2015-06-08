GitHubTarballPackage('mono', 'mono-basic', '2.10', '1aaf4fdbc3952776e0d4549b280b784faeffd7ec',
                     configure='./configure --prefix="%{prefix}"',
                     override_properties={'make': 'make'}
                     )
