Package('libsamplerate', '0.1.8',
        sources=[
            'http://www.mega-nerd.com/SRC/%{name}-%{version}.tar.gz'
        ],

        # banshee's lastfmfingerprint addin requires
        # the single-precision variant
        configure_flags=['--enable-single']
        )
