#
# NOTE:	- building is memory consuming (up to c.a. 537MB)
# TODO:	- install manpages via makefile
#
# Conditional build:
%bcond_without	alsa	# ALSA audio driver (OSS otherwise)
#
Summary:	flite - a small, fast speech synthesis engine
Summary(pl.UTF-8):	flite - mały, szybki silnik syntezy mowy
Summary(ru.UTF-8):	flite - маленькое, быстрое средство для синтеза речи
Name:		flite
Version:	2.2
Release:	2
License:	Custom, see COPYING
Group:		Applications/Sound
#Source0Download: https://github.com/festvox/flite/releases
Source0:	https://github.com/festvox/flite/archive/v%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	31f84ece0078906780f07942c0cd978c
# ALT Linux patches:
Patch0:		%{name}-link.patch
Patch1:		%{name}-fix-readonly-assignments.patch
# Debian patches:
Patch2:		%{name}-doc.patch
#
Patch5:		%{name}-fix-audiodriver-setup.patch
URL:		http://www.festvox.org/flite/
BuildRequires:	autoconf
BuildRequires:	automake
%{?with_alsa:BuildRequires:	alsa-lib-devel}
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
%setup -q
%patch -P0 -p1
%patch -P1 -p1
%patch -P2 -p1
%patch -P5 -p1

%build
cp -f /usr/share/automake/config.sub .
%{__autoconf}
%configure \
	--enable-shared \
	--with-audio=%{?with_alsa:alsa}%{!?with_alsa:oss} \
	--with-vox=cmu_us_kal16

%{__make} -j1

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_mandir}/man1

%{__make} -j1 install \
	DESTDIR=$RPM_BUILD_ROOT

# omitted in make install
install bin/t2p $RPM_BUILD_ROOT%{_bindir}
cp -p debian/*.1 $RPM_BUILD_ROOT%{_mandir}/man1

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc ACKNOWLEDGEMENTS COPYING README.md doc/html
%attr(755,root,root) %{_bindir}/flite
%attr(755,root,root) %{_bindir}/flite_cmu_time_awb
%attr(755,root,root) %{_bindir}/flite_cmu_us_awb
%attr(755,root,root) %{_bindir}/flite_cmu_us_kal
%attr(755,root,root) %{_bindir}/flite_cmu_us_kal16
%attr(755,root,root) %{_bindir}/flite_cmu_us_rms
%attr(755,root,root) %{_bindir}/flite_cmu_us_slt
%attr(755,root,root) %{_bindir}/flite_time
%attr(755,root,root) %{_bindir}/t2p
%attr(755,root,root) %{_libdir}/libflite.so.*.*
%attr(755,root,root) %ghost %{_libdir}/libflite.so.1
%attr(755,root,root) %{_libdir}/libflite_cmu_grapheme_lang.so.*.*
%attr(755,root,root) %ghost %{_libdir}/libflite_cmu_grapheme_lang.so.1
%attr(755,root,root) %{_libdir}/libflite_cmu_grapheme_lex.so.*.*
%attr(755,root,root) %ghost %{_libdir}/libflite_cmu_grapheme_lex.so.1
%attr(755,root,root) %{_libdir}/libflite_cmu_indic_lang.so.*.*
%attr(755,root,root) %ghost %{_libdir}/libflite_cmu_indic_lang.so.1
%attr(755,root,root) %{_libdir}/libflite_cmu_indic_lex.so.*.*
%attr(755,root,root) %ghost %{_libdir}/libflite_cmu_indic_lex.so.1
%attr(755,root,root) %{_libdir}/libflite_cmu_time_awb.so.*.*
%attr(755,root,root) %ghost %{_libdir}/libflite_cmu_time_awb.so.1
%attr(755,root,root) %{_libdir}/libflite_cmu_us_awb.so.*.*
%attr(755,root,root) %ghost %{_libdir}/libflite_cmu_us_awb.so.1
%attr(755,root,root) %{_libdir}/libflite_cmu_us_kal.so.*.*
%attr(755,root,root) %ghost %{_libdir}/libflite_cmu_us_kal.so.1
%attr(755,root,root) %{_libdir}/libflite_cmu_us_kal16.so.*.*
%attr(755,root,root) %ghost %{_libdir}/libflite_cmu_us_kal16.so.1
%attr(755,root,root) %{_libdir}/libflite_cmu_us_rms.so.*.*
%attr(755,root,root) %ghost %{_libdir}/libflite_cmu_us_rms.so.1
%attr(755,root,root) %{_libdir}/libflite_cmu_us_slt.so.*.*
%attr(755,root,root) %ghost %{_libdir}/libflite_cmu_us_slt.so.1
%attr(755,root,root) %{_libdir}/libflite_cmulex.so.*.*
%attr(755,root,root) %ghost %{_libdir}/libflite_cmulex.so.1
%attr(755,root,root) %{_libdir}/libflite_usenglish.so.*.*
%attr(755,root,root) %ghost %{_libdir}/libflite_usenglish.so.1
%{_mandir}/man1/flite.1*
%{_mandir}/man1/flite_time.1*
%{_mandir}/man1/t2p.1*

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libflite.so
%attr(755,root,root) %{_libdir}/libflite_cmu_grapheme_lang.so
%attr(755,root,root) %{_libdir}/libflite_cmu_grapheme_lex.so
%attr(755,root,root) %{_libdir}/libflite_cmu_indic_lang.so
%attr(755,root,root) %{_libdir}/libflite_cmu_indic_lex.so
%attr(755,root,root) %{_libdir}/libflite_cmu_time_awb.so
%attr(755,root,root) %{_libdir}/libflite_cmu_us_awb.so
%attr(755,root,root) %{_libdir}/libflite_cmu_us_kal.so
%attr(755,root,root) %{_libdir}/libflite_cmu_us_kal16.so
%attr(755,root,root) %{_libdir}/libflite_cmu_us_rms.so
%attr(755,root,root) %{_libdir}/libflite_cmu_us_slt.so
%attr(755,root,root) %{_libdir}/libflite_cmulex.so
%attr(755,root,root) %{_libdir}/libflite_usenglish.so
%{_includedir}/flite

%files static
%defattr(644,root,root,755)
%{_libdir}/libflite.a
%{_libdir}/libflite_cmu_grapheme_lang.a
%{_libdir}/libflite_cmu_grapheme_lex.a
%{_libdir}/libflite_cmu_indic_lang.a
%{_libdir}/libflite_cmu_indic_lex.a
%{_libdir}/libflite_cmu_time_awb.a
%{_libdir}/libflite_cmu_us_awb.a
%{_libdir}/libflite_cmu_us_kal.a
%{_libdir}/libflite_cmu_us_kal16.a
%{_libdir}/libflite_cmu_us_rms.a
%{_libdir}/libflite_cmu_us_slt.a
%{_libdir}/libflite_cmulex.a
%{_libdir}/libflite_usenglish.a
