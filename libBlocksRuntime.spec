Summary:	The runtime library for C blocks support
Summary(pl.UTF-8):	Biblioteka uruchomieniowa do obsługi bloków w C
Name:		libBlocksRuntime
Version:	0.3
Release:	1
License:	MIT-like
Group:		Libraries
Source0:	http://downloads.sourceforge.net/blocksruntime/%{name}-%{version}.tar.gz
# Source0-md5:	9731dac1aff89a65ba0cb83ad5da9cda
URL:		http://sourceforge.net/projects/blocksruntime/
BuildRequires:	clang
BuildRequires:	ruby
BuildRequires:	sed >= 4.0
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This package contains the runtime library for C blocks support. Blocks
are a proposed extension to the C, Objective C, and C++ languages
developed by Apple to support the Grand Central Dispatch concurrency
engine.

%description -l pl.UTF-8
Ten pakiet zawiera bibliotekę uruchomieniową do obsługi bloków w C.
Bloki (Block) to proponowane rozszerzenie do języków C, Objective C
oraz C++, stworzone przez firmę Apple jako wsparcie dla silnika
współbierzności Grand Central Dispatch.

%package devel
Summary:	Header files for BlocksRuntime library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki BlocksRuntime
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
Header files for BlocksRuntime library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki BlocksRuntime.

%package static
Summary:	Static BlocksRuntime library
Summary(pl.UTF-8):	Statyczna biblioteka BlocksRuntime
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static BlocksRuntime library.

%description static -l pl.UTF-8
Statyczna biblioteka BlocksRuntime.

%prep
%setup -q

%build
# NOTE: not autoconf configure
CC="clang" \
./configure \
	--build=%{_target_platform} \
	--prefix=%{_prefix} \
	--libdir=%{_libdir}

# setup soname
%{__sed} -i -e 's@-shared@-shared -Wl,-soname,libBlocksRuntime.so.0@' Makefile

%{__make} \
	CFLAGS="%{rpmcflags}" \
	LDFLAGS="%{rpmldflags}"

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

chmod +x $RPM_BUILD_ROOT%{_libdir}/lib*.so*
ln -s libBlocksRuntime.so.0.0 $RPM_BUILD_ROOT%{_libdir}/libBlocksRuntime.so.0
ln -s libBlocksRuntime.so.0.0 $RPM_BUILD_ROOT%{_libdir}/libBlocksRuntime.so
install libBlocksRuntime.a $RPM_BUILD_ROOT%{_libdir}

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libBlocksRuntime.so.*.*
%attr(755,root,root) %ghost %{_libdir}/libBlocksRuntime.so.0

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libBlocksRuntime.so
%{_includedir}/Block.h
%{_includedir}/Block_private.h

%files static
%defattr(644,root,root,755)
%{_libdir}/libBlocksRuntime.a
