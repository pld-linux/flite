#
# NOTE:	- building is memory consuming (up to c.a. 537MB)
# TODO:	- review -link, version patches
#	- --disable-static doesn't work
#	- install manpages via makefile
#
# Conditional build:
%bcond_without	static_libs # don't pack static liraries
#
Summary:	flite - a small, fast speech synthesis engine
Summary(pl.UTF-8):	flite - mały, szybki silnik syntezy mowy
Summary(ru.UTF-8):	flite - маленькое, быстрое средство для синтеза речи
Name:		flite
Version:	1.2
Release:	3
License:	Custom, see COPYING
Group:		Applications/Sound
Source0:	http://www.speech.cs.cmu.edu/flite/packed/flite-1.2/%{name}-%{version}-release.tar.bz2
# Source0-md5:	24c1576f5b3eb23ecedf4bebde96710f
# ALT Linux patches:
Patch0:		%{name}-link.patch
Patch1:		%{name}-fix-readonly-assignments.patch
# Debian patches:
Patch2:		%{name}-doc.patch
Patch3:		%{name}-version.patch
#
Patch4:		%{name}-DESTDIR.patch
Patch5:		%{name}-fix-audiodriver-setup.patch
Patch6:		%{name}-so_link.patch
URL:		http://cmuflite.org/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	alsa-lib-devel
BuildRequires:	ed
BuildRequires:	tetex
BuildRequires:	texi2html
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Flite - a small, fast speech synthesis engine. It is the latest
addition to the suite of free software synthesis tools including
University of Edinburgh's Festival Speech Synthesis System and
Carnegie Mellon University's FestVox project, tools, scripts and
documentation for building synthetic voices. However, flite itself
does not require either of these systems to compile and run.

%description -l pl.UTF-8
Flite to mały, szybki silnik syntezy mowy. Jest najnowszym dodatkiem
do zestawu wolnodostępnych narzędzi do syntezy zawierającego system
syntezy mowy Festival z University of Edinburgh, projekt FestVox z
Carnegie Mellon University, narzędzia, skrypty i dokumentację
tworzenia głosów syntetycznych. Jednak sam flite nie wymaga żadnego z
tych systemów do skompilowania czy uruchomienia.

%description -l ru.UTF-8
Flite -- маленькое, быстрое средство для синтеза речи. Это последнее
добавление к набору свободного программного обеспечения для синтеза
речи, проекты FestVox и Festival. Однако, сам flite не требует ни
одного из этих пакетов для компиляции и запуска.

%package devel
Summary:	Development files for flite
Summary(pl.UTF-8):	Pliki programistyczne dla flite
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
Development files for flite, a small, fast speech synthesis engine.

%description devel -l pl.UTF-8
Pliki programistyczne dla flite - małego, szybkiego silnika syntezy
mowy.

%description devel -l ru.UTF-8
Файлы для разработки с использованием flite - маленького, быстрого
средства для синтеза речи.

%package static
Summary:	Static flite library
Summary(pl.UTF-8):	Statyczna biblioteka flite
Group:		Applications/Sound
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static library for flite, a small, fast speech synthesis engine.

%description static -l pl.UTF-8
Statyczna biblioteka flite - małego, szybkiego silnika syntezy mowy.

%description static -l ru.UTF-8
Статические файлы для разработки с использованием flite - маленького,
быстрого средства для синтеза речи.

%prep
%setup -qn %{name}-%{version}-release
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1
%patch6 -p0

%build
cp -f /usr/share/automake/config.sub .
%{__autoconf}
%configure \
	--with-audio=oss \
	--enable-shared \
	%{!?with_static_libs:--disable-static} \
	--with-vox=cmu_us_kal16

%{__make} -j1

%install
rm -rf $RPM_BUILD_ROOT
# temp. workaround - put manpages in better place and install them via Makefile
install -d $RPM_BUILD_ROOT%{_mandir}/man1

%{__make} -j1 install \
	DESTDIR=$RPM_BUILD_ROOT

install debian/*.1 $RPM_BUILD_ROOT%{_mandir}/man1

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc ACKNOWLEDGEMENTS README COPYING doc/html
%attr(755,root,root) %{_bindir}/*
%attr(755,root,root) %{_libdir}/lib*.so.*.*
%attr(755,root,root) %ghost %{_libdir}/lib*.so.[0-9]
%{_mandir}/man1/*.1*

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/lib*.so
%{_includedir}/*

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/lib*.a
%endif
