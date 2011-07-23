Name:			opensonic
Summary:		A game based on the "Sonic the Hedgehog" universe
Version:		0.1.4
Release:		%mkrel 01
License:		GPL
Group:			Amusements/Games/Action/Arcade
URL:			http://opensnc.sourceforge.net/home/index.php
Source0:		opensnc-src-%{version}.tar.gz
Source1:		alpng13.tar.gz
BuildRoot:		%{_tmppath}/%{name}-%{version}-build
BuildRequires:	allegro-devel  logg
BuildRequires:	fdupes
BuildRequires:	cmake
BuildRequires:	dumb-devel
BuildRequires:	libogg-devel
BuildRequires:	libvorbis-devel


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
and timers. Currently this game works on Microsoft Windows and
GNU/Linux.



%prep
%setup -q -n opensnc-src-%{version}



%__install -dm 755 alpng
pushd alpng
	%__tar xfz %{SOURCE1}
popd


%build
pushd alpng
./configure
make 

popd
export OPENSNC_ALLEGRO_LIBS=`allegro-config --libs`
export OPENSNC_ALLEGRO_VERSION=`allegro-config --version`

./configure

%make 


%install
%makeinstall DESTDIR=%{buildroot}

%__install -dm 755 %{buildroot}%{_bindir}
%__cat > %{buildroot}%{_bindir}/%{name}.sh << EOF
#!/bin/bash
cd %{_datadir}/%{name}
pasuspender ./%{name}
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
EOF


chmod 777 %{buildroot}%{_bindir}/%{name}.sh
chmod 777 %{buildroot}%{_datadir}/%{name}/%{name}
%clean


%files
%defattr(-,root,root)
%doc *.html license.txt
%{_datadir}/applications/%{name}.desktop
%{_datadir}/pixmaps/*.png

%defattr(664,root,games,775)
%dir %{_datadir}/%{name}/config
%{_datadir}/%{name}/config/*
%dir %{_datadir}/%{name}/images
%{_datadir}/%{name}/images/*
%dir %{_datadir}/%{name}/languages
%{_datadir}/%{name}/languages/*
%dir %{_datadir}/%{name}/levels
%{_datadir}/%{name}/levels/*
%dir %{_datadir}/%{name}/licenses
%{_datadir}/%{name}/licenses/*
%dir %{_datadir}/%{name}/musics
%{_datadir}/%{name}/musics/*
%dir %{_datadir}/%{name}/quests
%{_datadir}/%{name}/quests/*
%dir %{_datadir}/%{name}/samples
%{_datadir}/%{name}/samples/*
%dir %{_datadir}/%{name}/themes
%{_datadir}/%{name}/*
%dir %{_datadir}/%{name}/screenshots
%defattr(777,root,root)
%{_bindir}/%{name}.sh
%{_datadir}/%{name}/%{name}


