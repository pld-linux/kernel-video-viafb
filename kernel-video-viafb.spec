#
# Conditional build:
%bcond_without	dist_kernel	# allow non-distribution kernel
%bcond_without	kernel		# don't build kernel modules
%bcond_without	smp		# don't build SMP module
%bcond_with	verbose		# verbose build (V=1)

%if %{without kernel}
%undefine	with_dist_kernel
%endif

# see kernel.spec
%ifarch sparc
%undefine	with_smp
%endif

%define		_rel	1
Summary:	VIA Unichrome framebuffer driver for Linux
Summary(pl):	Sterownik framebuffera dla kart VIA Unichrome dla Linuksa
Name:		kernel-video-viafb
Version:	2.6.00.02a
Release:	%{_rel}@%{_kernel_ver_str}
License:	distributable
Group:		Base/Kernel
Source0:	http://www.viaarena.com/Driver/linux-fbdev-kernel-src_%{version}.tgz
# Source0-md5:	0b1c68388f0d2cba8e4938293f7fbe5b
Patch0:		%{name}-Makefile.patch
%if %{with kernel}
%{?with_dist_kernel:BuildRequires:	kernel-module-build >= 3:2.6.14}
BuildRequires:	rpmbuild(macros) >= 1.217
%endif
BuildRequires:	sed >= 4.0
Requires(post,postun):	/sbin/depmod
%if %{with dist_kernel}
%requires_releq_kernel_up
Requires(postun):	%releq_kernel_up
%endif
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This is the console framebuffer driver for Graphics chips of VIA
UniChrome Family (CLE266, KM400, KN400, KM800, KN800, PM800, PN800,
CN400, CN700, CX700).

This package contains Linux kernel module.

%description -l pl
To jest sterownik do obs³ugi framebuffera dla kart graficznych z
rodziny VIA Unichrome (CLE266, KM400, KN400, KM800, KN800, PM800,
PN800, CN400, CN700, CX700).

Ten pakiet zawiera modu³ j±dra Linuksa.

%package -n kernel-smp-video-viafb
Summary:	VIA Unichrome framebuffer driver for Linux SMP
Summary(pl):	Sterownik framebuffera dla kart VIA Unichrome dla Linuksa SMP
Release:	%{_rel}@%{_kernel_ver_str}
Group:		Base/Kernel
Requires(post,postun):	/sbin/depmod
%if %{with dist_kernel}
%requires_releq_kernel_smp
Requires(postun):	%releq_kernel_smp
%endif

%description -n kernel-smp-video-viafb
This is the console framebuffer driver for Graphics chips of VIA
UniChrome Family (CLE266, KM400, KN400, KM800, KN800, PM800, PN800,
CN400, CN700, CX700).

This package contains Linux SMP kernel module.

%description -n kernel-smp-video-viafb -l pl
To jest sterownik do obs³ugi framebuffera dla kart graficznych z
rodziny VIA Unichrome (CLE266, KM400, KN400, KM800, KN800, PM800,
PN800, CN400, CN700, CX700).

Ten pakiet zawiera modu³ j±dra Linuksa SMP.

%prep
%setup -q -n Linux-FBDev-kernel-src_%{version}
%patch0 -p1
cp -f Makefile_26_Lite.kernel Makefile

%build
%if %{with kernel}
# kernel module(s)
for cfg in %{?with_dist_kernel:%{?with_smp:smp} up}%{!?with_dist_kernel:nondist}; do
	if [ ! -r "%{_kernelsrcdir}/config-$cfg" ]; then
		exit 1
	fi
	rm -rf include
	install -d o/include/linux
	ln -sf %{_kernelsrcdir}/config-$cfg o/.config
	ln -sf %{_kernelsrcdir}/Module.symvers-$cfg o/Module.symvers
	ln -sf %{_kernelsrcdir}/include/linux/autoconf-$cfg.h o/include/linux/autoconf.h
%if %{with dist_kernel}
	%{__make} -j1 -C %{_kernelsrcdir} O=$PWD/o prepare scripts
%else
	install -d o/include/config
	touch o/include/config/MARKER
	ln -sf %{_kernelsrcdir}/scripts o/scripts
%endif
#
#	patching/creating makefile(s) (optional)
#
	%{__make} -C %{_kernelsrcdir} clean \
		RCS_FIND_IGNORE="-name '*.ko' -o" \
		SYSSRC=%{_kernelsrcdir} \
		SYSOUT=$PWD/o \
		M=$PWD O=$PWD/o \
		%{?with_verbose:V=1}
	%{__make} -C %{_kernelsrcdir} modules \
		CC="%{__cc}" CPP="%{__cpp}" \
		SYSSRC=%{_kernelsrcdir} \
		SYSOUT=$PWD/o \
		M=$PWD O=$PWD/o \
		%{?with_verbose:V=1}
	mv viafb{,-$cfg}.ko
done
%endif

%install
rm -rf $RPM_BUILD_ROOT

%if %{with kernel}
install -d $RPM_BUILD_ROOT/lib/modules/%{_kernel_ver}{,smp}/video
install viafb-%{?with_dist_kernel:up}%{!?with_dist_kernel:nondist}.ko \
	$RPM_BUILD_ROOT/lib/modules/%{_kernel_ver}/video/viafb.ko
%if %{with smp} && %{with dist_kernel}
install viafb-smp.ko \
	$RPM_BUILD_ROOT/lib/modules/%{_kernel_ver}smp/video/viafb.ko
%endif
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%post
%depmod %{_kernel_ver}

%postun
%depmod %{_kernel_ver}

%post	-n kernel-smp-video-viafb
%depmod %{_kernel_ver}smp

%postun	-n kernel-smp-video-viafb
%depmod %{_kernel_ver}smp

%if %{with kernel}
%files
%defattr(644,root,root,755)
%doc readme.txt viafb.modes
/lib/modules/%{_kernel_ver}/video/*.ko*

%if %{with smp} && %{with dist_kernel}
%files -n kernel-smp-video-viafb
%defattr(644,root,root,755)
%doc readme.txt viafb.modes
/lib/modules/%{_kernel_ver}smp/video/*.ko*
%endif
%endif
