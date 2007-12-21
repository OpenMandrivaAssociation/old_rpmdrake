##################################################################
#
#
# !!!!!!!! WARNING => THIS HAS TO BE EDITED IN THE CVS !!!!!!!!!!!
#
#
##################################################################

%define name old_rpmdrake
%define version 2.27.1
%define release %mkrel 5

Name: %{name}
Version: %{version}
Release: %{release}
License: GPL
Source0: %name-%version.tar.bz2
Source1: base.png
Patch0:	 old_rpmdrake-use-another-config-file.patch
Summary: Mandriva Linux graphical front end for sofware installation/removal
Requires: perl-MDK-Common >= 1.1.18-2mdk
Requires: urpmi >= 4.8.4
Requires: perl-URPM >= 1.20
Requires: drakxtools >= 10.4.5
Requires: rpmtools >= 5.0.5
Requires: packdrake >= 5.0.5
Requires: perl-Gtk2 >= 1.054-1mdk
Requires: perl-Locale-gettext >= 1.01-7mdk
Requires: rpmdrake
# for now, packdrake (5.0.9) works better with this
Requires: perl-Compress-Zlib >= 1.33
BuildRequires: perl-devel
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot
Group: System/Configuration/Packaging
URL: http://cvs.mandriva.com/cgi-bin/cvsweb.cgi/soft/rpmdrake/
Obsoletes: MandrakeUpdate
Provides: MandrakeUpdate
Conflicts: drakconf < 10.1-4mdk

%description
rpmdrake is a simple graphical frontend to manage software packages on a
Mandriva Linux system; it has 3 different modes:
- software packages installation;
- software packages removal;
- MandrivaUpdate (software packages updates).

A fourth program manages the media (add, remove, edit).

%prep
rm -rf $RPM_BUILD_ROOT

%setup -q
%patch0 -p0

%build
make OPTIMIZE="$RPM_OPT_FLAGS -Wall" PREFIX=%{_prefix} INSTALLDIRS=vendor

%install
make install PREFIX=%buildroot/%{_prefix} BINDIR=%buildroot/%{_bindir} SBINDIR=%buildroot/%{_sbindir} DESTDIR=%buildroot
mkdir -p $RPM_BUILD_ROOT/{%{perl_vendorlib}/old_urpm,usr/lib/libDrakX}
install -m 644 old_rpmdrake.pm $RPM_BUILD_ROOT/%{perl_vendorlib}
install -m 644 old_urpm.pm $RPM_BUILD_ROOT/%{perl_vendorlib}
install -m 644 old_urpm/*.pm $RPM_BUILD_ROOT/%{perl_vendorlib}/old_urpm
install -m 644 old_ugtk2.pm $RPM_BUILD_ROOT/usr/lib/libDrakX

mkdir -p $RPM_BUILD_ROOT/%_datadir/rpmdrake/icons
install -m 644 %SOURCE1 $RPM_BUILD_ROOT/%_datadir/rpmdrake/icons/base.png

mkdir -p $RPM_BUILD_ROOT%{_menudir}
cp %{name}.menu $RPM_BUILD_ROOT%{_menudir}/%{name}
mkdir -p $RPM_BUILD_ROOT%{_datadir}/applications/
cat > $RPM_BUILD_ROOT%{_datadir}/applications/mandriva-oldrpmdrake.desktop << EOF
[Desktop Entry]
Name=Browse Available Software (old)
Comment=A graphical front end for installing, removing and updating packages (old)
Exec=/usr/sbin/rpmdrake
Icon=/usr/share/icons/rpmdrake.png
Type=Application
Categories=X-MandrivaLinux-CrossDesktop;GTK;System;PackageManager;
NoDisplay=true
EOF

cat > $RPM_BUILD_ROOT%{_datadir}/applications/mandriva-oldrpmdrake-root.desktop << EOF
[Desktop Entry]
Name=Install, Remove & Update Software (old)
Comment=A graphical front end for installing, removing and updating packages (old)
Exec=old_rpmdrake
Icon=/usr/share/icons/rpmdrake.png
Type=Application
Categories=X-MandrivaLinux-CrossDesktop;GTK;System;PackageManager;
NoDisplay=true
EOF

%clean
rm -rf $RPM_BUILD_ROOT

%post 
%update_menus

%postun
%clean_menus

%files 
%defattr(-, root, root)
%doc COPYING AUTHORS README ChangeLog
%{_sbindir}/old*
%{_bindir}/*
%{perl_vendorlib}/*
%{_menudir}/%{name}
%{_datadir}/applications/mandriva-*.desktop
/usr/lib/libDrakX/old_ugtk2.pm
%_datadir/rpmdrake/icons/base.png


