%define mdmpd_version 0.4

%ifarch %{ix86} ppc ppc64 %{sunsparc}
%bcond_without dietlibc
%define dietlibc_req %{nil}
%endif
%ifarch x86_64
%bcond_without dietlibc
%define dietlibc_req >= 0.29-1mdk
%endif

%bcond_with uclibc
%bcond_with klibc
%bcond_with mdassemble_auto
%bcond_with mdmpd

%if %{with mdassemble_auto}
%define mdassemble_auto_CFLAGS MDASSEMBLE_AUTO=1
%else
%define mdassemble_auto_CFLAGS %{nil}
%endif

# we want to install in /sbin, not /usr/sbin...
%define _exec_prefix %{nil}

Name:           mdadm
Version:        2.6.4
Release:        %mkrel 1
Summary:        A tool for managing Soft RAID under Linux
Group:          System/Kernel and hardware
License:        GPL
URL:            http://www.cse.unsw.edu.au/~neilb/source/mdadm/
Source0:        http://www.cse.unsw.edu.au/~neilb/source/mdadm/mdadm-%{version}.tgz
Source1:        mdadm.init
Source2:        raidtabtomdadm.sh
Source3:        mdmpd-%{mdmpd_version}.tar.bz2
Source4:        mdmpd.init
Patch0:         mdadm-2.6.2-werror.patch
Patch1:         mdmpd-0.3-pid.patch
Patch2:         mdmpd-0.4-gcc4.patch
Patch3:         mdadm-2.5.1-autof.patch
Requires(post): gawk
Requires(post): rpm-helper
Requires(preun): rpm-helper
BuildRequires:  groff-for-man
%if %{with dietlibc}
BuildRequires:  dietlibc-devel %{dietlibc_req}
%endif
%if %{with uclibc}
BuildRequires:  uClibc-devel
%endif
%if %{with klibc}
BuildRequires:  klibc-devel
%endif

%description
mdadm is a program that can be used to create, manage, and monitor
Linux MD (Software RAID) devices.

As such is provides similar functionality to the raidtools packages.
The particular differences to raidtools is that mdadm is a single
program, and it can perform (almost) all functions without a
configuration file (that a config file can be used to help with
some common tasks).

%package -n mdmpd
Summary:        daemon to monitor MD multipath devices
Group:          System/Kernel and hardware

%description -n mdmpd
This daemon will monitor md multipath devices for failure and recovery of
device paths, in order to add paths back upon recovery. It requires a patched
kernel with support for events in /proc/mdstat.

%prep
%setup -q -a 3
%patch0 -p1
%patch1 -p0
%patch2 -p0
%patch3 -p1
%{__perl} -pi -e 's/-Werror//' Makefile
OPT_FLAGS=`/bin/echo %{optflags} | %{__sed} -e 's/-fstack-protector//'`
%{__perl} -pi -e "s/^CXFLAGS = .*/CXFLAGS = $OPT_FLAGS/" Makefile
cp %{SOURCE2} raidtabtomdadm.sh

%build
%if %{with dietlibc}
%if %{with uclibc} || %{with klibc}
%{error:only one of dietlibc, uclibc or klibc can be specified}
exit 1
%endif
%{make} mdassemble %{mdassemble_auto_CFLAGS} SYSCONFDIR="%{_sysconfdir}"
%endif
%if %{with uclibc}
%if %{with klibc}
%{error:only one of dietlibc, uclibc or klibc can be specified}
exit 1
%endif
%{make} mdadm.uclibc mdassemble.uclibc %{mdassemble_auto_CFLAGS} SYSCONFDIR="%{_sysconfdir}"
%endif
%if %{with klibc}
%{make} mdassemble.klibc %{mdassemble_auto_CFLAGS} SYSCONFDIR="%{_sysconfdir}"
%endif
%{make} SYSCONFDIR="%{_sysconfdir}"
%if %{with mdmpd}
%{make} -C mdmpd CCFLAGS="%{optflags} -I." SYSCONFDIR="%{_sysconfdir}"
%endif

%install
rm -rf %{buildroot}

%{makeinstall_std} MANDIR=%{_mandir} BINDIR=%{_sbindir}
%if %{with mdmpd}
%{makeinstall_std} -C mdmpd MANDIR=%{_mandir} BINDIR=%{_sbindir}
%endif
install -D -m 644 mdadm.conf-example %{buildroot}%{_sysconfdir}/mdadm.conf

install -D %{SOURCE1} %{buildroot}%{_initrddir}/mdadm
%if %{with mdmpd}
install -D %{SOURCE4} %{buildroot}%{_initrddir}/mdmpd
mkdir -p %{buildroot}/var/run/mdmpd
%endif

%if %{with dietlibc}
install mdassemble %{buildroot}%{_sbindir}/mdassemble
install -D -m 644 mdassemble.8 %{buildroot}%{_mandir}/man8/mdassemble.8
%endif
%if %{with uclibc}
install mdassemble.uclibc %{buildroot}%{_sbindir}/mdassemble
install -D -m 644 mdassemble.8 %{buildroot}%{_mandir}/man8/mdassemble.8
%endif
%if %{with klibc}
install mdassemble.klibc %{buildroot}%{_sbindir}/mdassemble
install -D -m 644 mdassemble.8 %{buildroot}%{_mandir}/man8/mdassemble.8
%endif

#install -D -m 755 mkinitramfs %{buildroot}%{_sbindir}/mkinitramfs

%clean
rm -rf %{buildroot}

%preun
%_preun_service mdadm

%if %{with mdmpd}
%preun -n mdmpd
%_preun_service mdmpd
%endif

%post -f raidtabtomdadm.sh
%_post_service mdadm

%if %{with mdmpd}
%post -n mdmpd
%_post_service mdmpd
%endif

%files
%defattr(644,root,root,755)
%doc TODO ChangeLog mdadm.conf-example README.initramfs ANNOUNCE*
%attr(755,root,root) %{_sbindir}/mdadm
#attr(755,root,root) %{_sbindir}/mkinitramfs
%if %{with dietlibc} || %{with uclibc} || %{with klibc}
%attr(755,root,root) %{_sbindir}/mdassemble
%endif
%config(noreplace,missingok) %{_sysconfdir}/mdadm.conf
%attr(755,root,root) %{_initrddir}/mdadm
%{_mandir}/man*/md*

%if %{with mdmpd}
%files -n mdmpd
%attr(755,root,root) %{_sbindir}/mdmpd
%attr(755,root,root) %{_initrddir}/mdmpd
%dir /var/run/mdmpd
%endif
