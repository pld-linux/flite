#
# NOTE:	- building is memory consuming (up to c.a. 537MB)
# TODO:	- review -link,-alsa, version patches
#	- --disable-static doesn't work
#	- install manpages via makefile
#
# Conditional build:
%bcond_without	static_libs # don't pack static liraries
#
Name:		flite
Version:	1.2
Release:	0.1
Summary:	flite - a small, fast speech synthesis engine
Summary(ru_RU.KOI8-R):flite - маленькое, быстрое средство для синтеза речи
License:	Custom, see COPYING
Group:		Applications/Sound
Source0:	http://www.speech.cs.cmu.edu/flite/packed/flite-1.2/%{name}-%{version}-release.tar.bz2
# Source0-md5:	24c1576f5b3eb23ecedf4bebde96710f
# ALT Linux patches:
Patch0:		%{name}-link.patch
Patch1:		%{name}-alsa.patch
Patch2:		%{name}-DESTDIR.patch
Patch3:		%{name}-fix-readonly-assignments.patch
# Debian patches:
Patch4:		%{name}-doc.patch
Patch5:		%{name}-version.patch
URL:		http://cmuflite.org/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	alsa-lib-devel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Flite - a small, fast speech synthesis engine. It is the latest
addition to the suite of free software synthesis tools including
University of Edinburgh's Festival Speech Synthesis System and
Carnegie Mellon University's FestVox project, tools, scripts and
documentation for building synthetic voices. However, flite itself
does not require either of these systems to compile and run.

%description -l ru_RU.KOI8-R
Flite -- маленькое, быстрое средство для синтеза речи. Это последнее
добавление к набору свободного программного обеспечения для синтеза
речи, проекты FestVox и Festival. Однако, сам flite не требует ни
одного из этих пакетов для компиляции и запуска.

%package devel
Summary:	development files for flite
Group:		Applications/Sound
Requires:	%{name} = %{version}-%{release}

%description devel
development files for flite, a small, fast speech synthesis engine

%description devel -l ru_RU.KOI8-R
Файлы для разработки с использованием flite - маленького, быстрого
средства для синтеза речи.

%package static
Summary:	static development files for flite
Group:		Applications/Sound
Requires:	%{name}-devel = %{version}-%{release}

%description static
static development files for flite, a small, fast speech synthesis
engine

%description static -l ru_RU.KOI8-R
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

%build
cp -f /usr/share/automake/config.sub .
%{__autoconf}
%configure \
	--enable-shared \
	%{!?with_static_libs:--disable-static} \
	--with-vox=cmu_us_kal16

%{__make}

%install
rm -rf $RPM_BUILD_ROOT
# temp. workaround - put manpages in better place and install them via Makefile
install -d $RPM_BUILD_ROOT%{_mandir}/man1

%{__make} install \
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
%{_mandir}/man1/*.1*

%files devel
%defattr(644,root,root,755)
%{_includedir}/*
%attr(755,root,root) %{_libdir}/lib*.so

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/lib*.a
%endif
