%bcond_without	uclibc

Summary:	A tool for managing Soft RAID under Linux
Name:		mdadm
Version:	3.3
Release:	5
Group:		System/Kernel and hardware
License:	GPLv2+
Url:		http://www.kernel.org/pub/linux/utils/raid/mdadm/
Source0:	http://www.kernel.org/pub/linux/utils/raid/mdadm/mdadm-%{!?git:%version}%{?git:%git}.tar.xz
%if %{?git:0}%{?!git:1}
Source1:	http://www.kernel.org/pub/linux/utils/raid/mdadm/mdadm-%{version}.tar.sign
%endif
# From Fedora
Source3:	mdadm-raid-check
Source4:	mdadm-raid-check-sysconfig
Source5:	mdadm-cron
Source6:	mdadm.rules
Source7:	mdmonitor.service
Source8:	mdmonitor-takeover.service
Source9:	mdadm-tmpfiles.conf
Source10:	mdadm_event.conf
# in situations where only ntfw and not ftw is enabled with uClibc, it's
# assumed to have neither, which this patch fixes
Patch3:		mdadm-3.2.7-uclibc-make-ntfw-work-without-ftw-enabled.patch
# add support for compiling with -fwhole-program
Patch4:		mdadm-3.3-whole-program.patch

# Fedora patches
Patch101:	mdadm-3.3-Be-consistent-in-return-types-from-byteswap-macros.patch
Patch197:	mdadm-3.3-udev.patch

# udev rule used to be in udev package
BuildRequires:	groff
BuildRequires:	binutils-devel
BuildRequires:	systemd-units
%if %{with uclibc}
BuildRequires:	uClibc-devel >= 0.9.33.2-15
%endif
Requires(post,preun):	rpm-helper

%description
mdadm is a program that can be used to create, manage, and monitor
Linux MD (Software RAID) devices.

As such is provides similar functionality to the raidtools packages.
The particular differences to raidtools is that mdadm is a single
program, and it can perform (almost) all functions without a
configuration file (that a config file can be used to help with
some common tasks).

%package -n	uclibc-%{name}
Summary:	A tool for managing Soft RAID under Linux (uClibc build)
Group:		System/Kernel and hardware
Requires:	%{name} = %{EVRD}

%description -n	uclibc-%{name}
mdadm is a program that can be used to create, manage, and monitor
Linux MD (Software RAID) devices.

As such is provides similar functionality to the raidtools packages.
The particular differences to raidtools is that mdadm is a single
program, and it can perform (almost) all functions without a
configuration file (that a config file can be used to help with
some common tasks).

%prep
%setup -q %{?git:-n %{name}}
%apply_patches

echo "PROGRAM /sbin/mdadm-syslog-events" >> mdadm.conf-example
%if %{with uclibc}
mkdir .uclibc
pushd .uclibc
cp -a ../* .
popd
%endif

%build
%setup_compile_flags
%if %{with uclibc}
pushd .uclibc
make WHOLE_PROGRAM=1 CWFLAGS=-Wall CC="%{uclibc_cc}" SYSCONFDIR="%{_sysconfdir}" CXFLAGS="%{uclibc_cflags}"
popd
%endif

%make WHOLE_PROGRAM=1 CWFLAGS=-Wall SYSCONFDIR="%{_sysconfdir}" CXFLAGS="%{optflags}"

%install
%if %{with uclibc}
install -m755 .uclibc/mdadm -D %{buildroot}%{uclibc_root}/sbin/mdadm
install -m755 .uclibc/mdmon -D %{buildroot}%{uclibc_root}/sbin/mdmon
%endif

make install-man install-udev DESTDIR=%{buildroot} MANDIR=%{_mandir} BINDIR=/sbin
install -m755 mdadm -D %{buildroot}/sbin/mdadm
install -m755 mdmon -D %{buildroot}/sbin/mdmon


install -p -m644 mdadm.conf-example -D %{buildroot}%{_sysconfdir}/mdadm.conf
install -p -m755 %{SOURCE3} -D %{buildroot}%{_sbindir}/raid-check
install -p -m644 %{SOURCE4} -D %{buildroot}%{_sysconfdir}/sysconfig/raid-check
install -p -m644 %{SOURCE5} -D %{buildroot}%{_sysconfdir}/cron.d/raid-check
install -p -m755 misc/syslog-events -D %{buildroot}/sbin/mdadm-syslog-events
install -p -m644 %{SOURCE6} -D %{buildroot}/lib/udev/rules.d/65-md-incremental.rules

install -m644 %{SOURCE7} -D %{buildroot}%{_unitdir}/mdmonitor.service
install -m644 %{SOURCE8} -D %{buildroot}%{_unitdir}/mdmonitor-takeover.service
ln -s mdmonitor.service %{buildroot}%{_unitdir}/mdadm.service
install -m644 %{SOURCE9} -D %{buildroot}%{_prefix}/lib/tmpfiles.d/%{name}.conf
rm -rf %{buildroot}%{_initrddir}/mdadm

install -m644 %{SOURCE10} -D %{buildroot}%{_sysconfdir}/libreport/events.d/mdadm_event.conf

%files
%doc TODO ChangeLog README.initramfs ANNOUNCE*
/sbin/mdadm
/sbin/mdadm-syslog-events
/sbin/mdmon
%{_sbindir}/raid-check
%config(noreplace) %{_sysconfdir}/cron.d/raid-check
%config(noreplace,missingok) %{_sysconfdir}/mdadm.conf
%config(noreplace) %{_sysconfdir}/sysconfig/raid-check
/lib/udev/rules.d/63-md-raid-arrays.rules
/lib/udev/rules.d/64-md-raid-assembly.rules
/lib/udev/rules.d/65-md-incremental.rules
%{_unitdir}/*.service
%{_prefix}/lib/tmpfiles.d/%{name}.conf
%{_sysconfdir}/libreport/events.d/*
%{_mandir}/man*/md*

%if %{with uclibc}
%files -n uclibc-%{name}
%{uclibc_root}/sbin/mdadm
%{uclibc_root}/sbin/mdmon
%endif
