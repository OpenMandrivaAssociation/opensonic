Name:			opensonic
Summary:		A game based on the "Sonic the Hedgehog" universe
Version:		0.1.4
Release:		1
License:		GPL
Group:			Amusements/Games/Action/Arcade
URL:			https://opensnc.sourceforge.net/home/index.php
Source0:		https://prdownloads.sourceforge.net/opensnc/Open%20Sonic/%{version}/opensnc-src-%{version}.tar.gz
Source1:		https://prdownloads.sourceforge.net/alpng/alpng/1.3/alpng13.tar.gz
Source2:		https://opensnc.sourceforge.net/logg/logg-2.9.zip
BuildRequires:	allegro-devel
BuildRequires:	fdupes
BuildRequires:	cmake
BuildRequires:	ninja
BuildRequires:	dumb-devel
BuildRequires:	pkgconfig(ogg)
BuildRequires:	pkgconfig(vorbis)

%description
Open Sonic is a free open-source game based on the "Sonic the Hedgehog"
universe.

It introduces a different style of gameplay called cooperative play,
in which it's possible to control 3 characters simultaneously. Unlike
most similar games, Open Sonic provides a greater level of interaction
between the player and the levels. It's more than just a jump'n'run;
the user must come up with some strategy in order to get through the
levels.

Open Sonic is written from the ground up in C language and uses the
Allegro game programming library for graphics, sounds, player input
and timers.

%prep
%autosetup -p1 -n opensnc-src-%{version}
install -dm 755 alpng
pushd alpng
tar xf %{S:1}
popd
tar xf %{S:2}


%build
cd alpng
./configure
%make_build
cd ..

cd logg-2.9
make -f Makefile.unix FLAGS="%{optflags} -fPIC -fno-lto" CC=%{__cc}
cd ..

export _ALLEGRO_LIBS=`allegro-config --libs`
export _ALLEGRO_VERSION=`allegro-config --version`
export CFLAGS="%{optflags} -I$(pwd)/logg-2.9 -L$(pwd)/logg-2.9"
%cmake \
	-DLLOGG=`pwd`/liblogg.a \
	-G Ninja
%ninja_build 


%install
%ninja_install -C build

%__install -dm 755 %{buildroot}%{_bindir}
%__cat > %{buildroot}%{_bindir}/%{name}.sh << EOF
#!/bin/bash
cd %{_datadir}/%{name}
exec ./%{name}
EOF

# menu and icon
%__install -dm 755 %{buildroot}%{_datadir}/pixmaps
%__install -m 644 icon.png \
	%{buildroot}%{_datadir}/pixmaps/%{name}.png

%__install -dm 755 %{buildroot}%{_datadir}/applications
%__cat > %{buildroot}%{_datadir}/applications/%{name}.desktop << EOF
[Desktop Entry]
Comment=Open Sonic - A game based on the "Sonic the Hedgehog" universe
Name=Open Sonic
GenericName=Open Sonic
Type=Application
Exec=%{name}.sh
Icon=%{name}
Encoding=UTF-8
Categories=Game;ArcadeGame;
Path=%{_datadir}/%{name}
EOF


chmod 755 %{buildroot}%{_bindir}/%{name}.sh
chmod 755 %{buildroot}%{_datadir}/%{name}/%{name}


%files
%defattr(-,root,root)
%doc *.html license.txt
%{_datadir}/applications/%{name}.desktop
%{_datadir}/pixmaps/*.png
%{_datadir}/%{name}
%{_bindir}/%{name}.sh
