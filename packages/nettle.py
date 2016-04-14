Package('nettle', '2.5-pre', sources=[
    'http://www.lysator.liu.se/~nisse/archive/nettle-%{version}.tar.gz'
],
    configure_flags=['--enable-shared --disable-assembler']
)
