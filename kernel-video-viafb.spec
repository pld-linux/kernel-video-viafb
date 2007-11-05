#
# Conditional build:
%bcond_without	dist_kernel	# allow non-distribution kernel
%bcond_without	kernel		# don't build kernel modules
%bcond_with	verbose		# verbose build (V=1)

%if !%{with kernel}
%undefine	with_dist_kernel
%endif

%define		_rel	1
Summary:	VIA Unichrome framebuffer driver for Linux
Summary(pl.UTF-8):	Sterownik framebuffera dla kart VIA Unichrome dla Linuksa
Name:		kernel%{_alt_kernel}-video-viafb
Version:	2.6.00.03a
Release:	%{_rel}@%{_kernel_ver_str}
License:	distributable
Group:		Base/Kernel
Source0:	http://drivers.viaarena.com/linux-fbdev-kernel-src_%{version}.tgz
# Source0-md5:	b0b8a57431e6b0c7e9edbd56320b1cc1
%if %{with kernel}
%{?with_dist_kernel:BuildRequires:	kernel%{_alt_kernel}-module-build >= 3:2.6.20.2}
BuildRequires:	rpmbuild(macros) >= 1.379
%endif
BuildRequires:	sed >= 4.0
Requires(post,postun):	/sbin/depmod
%if %{with dist_kernel}
%requires_releq_kernel
Requires(postun):	%releq_kernel
%endif
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This is the console framebuffer driver for Graphics chips of VIA
UniChrome Family (CLE266, KM400, KN400, KM800, KN800, PM800, PN800,
CN400, CN700, CX700).

This package contains Linux kernel module.

%description -l pl.UTF-8
To jest sterownik do obsługi framebuffera dla kart graficznych z
rodziny VIA Unichrome (CLE266, KM400, KN400, KM800, KN800, PM800,
PN800, CN400, CN700, CX700).

Ten pakiet zawiera moduł jądra Linuksa.

%prep
%setup -q -n Linux-FBDev-kernel-src_%{version}
sed -e s/\$\(CONFIG_FB_VIA\)/m/ Makefile_26.kernel > Makefile

%build
%if %{with kernel}
%build_kernel_modules -m viafb
%endif

%install
rm -rf $RPM_BUILD_ROOT

%if %{with kernel}
%install_kernel_modules -m viafb -d kernel/drivers/video
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%post
%depmod %{_kernel_ver}

%postun
%depmod %{_kernel_ver}

%if %{with kernel}
%files
%defattr(644,root,root,755)
%doc readme.txt viafb.modes
/lib/modules/%{_kernel_ver}/kernel/drivers/video/*.ko*
%endif
