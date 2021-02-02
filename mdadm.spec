Summary:	A tool for managing Soft RAID under Linux
Name:		mdadm
Version:	4.1
Release:	10
Group:		System/Kernel and hardware
License:	GPLv2+
Url:		http://www.kernel.org/pub/linux/utils/raid/mdadm/
Source0:	http://www.kernel.org/pub/linux/utils/raid/mdadm/mdadm-%{version}.tar.xz
Source20:	61-dracut-distro-mdraid.conf
# fixes from uptream
Patch001:	0001-Assemble-keep-MD_DISK_FAILFAST-and-MD_DISK_WRITEMOST.patch
Patch002:	0002-Document-PART-POLICY-lines.patch
Patch003:	0003-policy-support-devices-with-multiple-paths.patch
Patch004:	0004-mdcheck-add-systemd-unit-files-to-run-mdcheck.patch
Patch005:	0005-Monitor-add-system-timer-to-run-oneshot-periodically.patch
Patch006:	0006-imsm-update-metadata-correctly-while-raid10-double-d.patch
Patch007:	0007-Assemble-mask-FAILFAST-and-WRITEMOSTLY-flags-when-fi.patch
Patch008:	0008-Grow-avoid-overflow-in-compute_backup_blocks.patch
Patch009:	0009-Grow-report-correct-new-chunk-size.patch
Patch010:	0010-policy.c-prevent-NULL-pointer-referencing.patch
Patch011:	0011-policy.c-Fix-for-compiler-error.patch
Patch012:	0012-imsm-finish-recovery-when-drive-with-rebuild-fails.patch
Patch013:	0013-imsm-fix-reshape-for-2TB-drives.patch
Patch014:	0014-Fix-spelling-typos.patch
Patch015:	0015-Detail.c-do-not-skip-first-character-when-calling-xs.patch
Patch016:	0016-Fix-reshape-for-decreasing-data-offset.patch
Patch017:	0017-mdadm-tests-add-one-test-case-for-failfast-of-raid1.patch
Patch018:	0018-mdmon-don-t-attempt-to-manage-new-arrays-when-termin.patch
Patch019:	0019-mdmon-wait-for-previous-mdmon-to-exit-during-takeove.patch
Patch020:	0020-Assemble-Fix-starting-array-with-initial-reshape-che.patch
Patch021:	0021-add-missing-units-to-examine.patch
Patch022:	0022-imsm-fix-spare-activation-for-old-matrix-arrays.patch
Patch023:	0023-Create-Block-rounding-size-to-max.patch
Patch024:	0024-udev-Add-udev-rules-to-create-by-partuuid-for-md-dev.patch
Patch025:	0025-mdmon-fix-wrong-array-state-when-disk-fails-during-m.patch
Patch026:	0026-Enable-probe_roms-to-scan-more-than-6-roms.patch
Patch027:	0027-super-intel-Fix-issue-with-abs-being-irrelevant.patch
Patch028:	0028-mdadm.h-Introduced-unaligned-get-put-_unaligned-16-3.patch
Patch029:	0029-super-intel-Use-put_unaligned-in-split_ull.patch
Patch030:	0030-mdadm-load-default-sysfs-attributes-after-assemblati.patch
Patch031:	0031-mdadm.h-include-sysmacros.h-unconditionally.patch
Patch032:	0032-mdadm-add-no-devices-to-avoid-component-devices-deta.patch
Patch033:	0033-udev-add-no-devices-option-for-calling-mdadm-detail.patch
Patch034:	0034-imsm-close-removed-drive-fd.patch
Patch035:	0035-mdadm-check-value-returned-by-snprintf-against-error.patch
Patch036:	0036-mdadm-Introduce-new-array-state-broken-for-raid0-lin.patch
Patch037:	0037-mdadm-force-a-uuid-swap-on-big-endian.patch
Patch038:	0038-mdadm-md.4-add-the-descriptions-for-bitmap-sysfs-nod.patch
Patch039:	0039-Init-devlist-as-an-array.patch
Patch040:	0040-Don-t-need-to-check-recovery-after-re-add-when-no-I-.patch
Patch041:	0041-udev-allow-for-udev-attribute-reading-bug.patch
Patch042:	0042-imsm-save-current_vol-number.patch
Patch043:	0043-imsm-allow-to-specify-second-volume-size.patch
Patch044:	0044-mdcheck-when-mdcheck_start-is-enabled-enable-mdcheck.patch
Patch045:	0045-mdcheck-use-to-pass-variable-to-mdcheck.patch
Patch046:	0046-SUSE-mdadm_env.sh-handle-MDADM_CHECK_DURATION.patch
Patch047:	0047-super-intel-don-t-mark-structs-packed-unnecessarily.patch
Patch048:	0048-Manage-Remove-the-legacy-code-for-md-driver-prior-to.patch
Patch049:	0049-Remove-last-traces-of-HOT_ADD_DISK.patch
Patch050:	0050-Fix-up-a-few-formatting-issues.patch
Patch051:	0051-Remove-unused-code.patch
Patch052:	0052-imsm-return-correct-uuid-for-volume-in-detail.patch
Patch053:	0053-imsm-Change-the-way-of-printing-nvme-drives-in-detai.patch
Patch054:	0054-Create-add-support-for-RAID0-layouts.patch
Patch055:	0055-Assemble-add-support-for-RAID0-layouts.patch
Patch056:	0056-Respect-CROSS_COMPILE-when-CC-is-the-default.patch
Patch057:	0057-Change-warning-message.patch
Patch058:	0058-mdcheck-service-can-t-start-succesfully-because-of-s.patch
Patch059:	0059-imsm-Update-grow-manual.patch
Patch060:	0060-Add-support-for-Tebibytes.patch
Patch061:	0061-imsm-fill-working_disks-according-to-metadata.patch
Patch062:	0062-mdadm.8-add-note-information-for-raid0-growing-opera.patch
Patch063:	0063-Remove-the-legacy-whitespace.patch
Patch064:	0064-imsm-pass-subarray-id-to-kill_subarray-function.patch
Patch065:	0065-imsm-Remove-dump-restore-implementation.patch

# From Fedora
Source3:	mdadm-raid-check
Source4:	mdadm-raid-check-sysconfig
Source5:	raid-check.timer
Source6:	raid-check.service
Source7:	mdadm.rules
Source8:	mdmonitor.service
Source9:	mdadm-tmpfiles.conf
Source10:	mdadm_event.conf

# Fedora patches
Patch198:	https://src.fedoraproject.org/rpms/mdadm/raw/master/f/mdadm-4.1-no-Werror.patch

# udev rule used to be in udev package
BuildRequires:	groff
BuildRequires:	binutils-devel
BuildRequires:	pkgconfig(systemd)
BuildRequires:	systemd-macros
Requires:	libreport-filesystem

%description
mdadm is a program that can be used to create, manage, and monitor
Linux MD (Software RAID) devices.

As such is provides similar functionality to the raidtools packages.
The particular differences to raidtools is that mdadm is a single
program, and it can perform (almost) all functions without a
configuration file (that a config file can be used to help with
some common tasks).

%prep
%autosetup -p1

printf '%s\n' "PROGRAM /sbin/mdadm-syslog-events" >> mdadm.conf-example

%build
%set_build_flags
%make_build CWFLAGS=-Wall SYSCONFDIR="%{_sysconfdir}" CXFLAGS="%{optflags} -fno-strict-aliasing"

%install
make install-man install-udev DESTDIR=%{buildroot} MANDIR=%{_mandir} BINDIR=/sbin SYSTEMD_DIR=%{_unitdir} install-systemd
install -m755 mdadm -D %{buildroot}/sbin/mdadm
install -m755 mdmon -D %{buildroot}/sbin/mdmon

install -p -m644 mdadm.conf-example -D %{buildroot}%{_sysconfdir}/mdadm.conf
install -p -m755 %{SOURCE3} -D %{buildroot}%{_sbindir}/raid-check
install -p -m644 %{SOURCE4} -D %{buildroot}%{_sysconfdir}/sysconfig/raid-check
install -p -m644 %{SOURCE5} -D %{buildroot}%{_unitdir}/raid-check.timer
install -p -m644 %{SOURCE6} -D %{buildroot}%{_unitdir}/raid-check.service
install -p -m755 misc/syslog-events -D %{buildroot}/sbin/mdadm-syslog-events
install -p -m644 %{SOURCE7} -D %{buildroot}%{_udevrulesdir}/65-md-incremental.rules
install -m644 %{SOURCE8} -D %{buildroot}%{_unitdir}/mdmonitor.service
install -m644 %{SOURCE9} -D %{buildroot}%{_tmpfilesdir}/%{name}.conf
install -m644 %{SOURCE10} -D %{buildroot}%{_sysconfdir}/libreport/events.d/mdadm_event.conf

install -d %{buildroot}%{_presetdir}
cat > %{buildroot}%{_presetdir}/86-%{name}.preset << EOF
enable mdmonitor.service
enable raid-check.timer
EOF

mkdir -p %{buildroot}%{_prefix}/lib/dracut/dracut.conf.d
cp %{S:20} %{buildroot}%{_prefix}/lib/dracut/dracut.conf.d/

%post
%systemd_post mdmonitor.service raid-check.timer

%preun
%systemd_preun mdmonitor.service raid-check.timer

%postun
%systemd_postun_with_restart mdmonitor.service

%files
%doc TODO ChangeLog README.initramfs ANNOUNCE*
/sbin/mdadm
/sbin/mdadm-syslog-events
/sbin/mdmon
%{_sbindir}/raid-check
%config(noreplace,missingok) %{_sysconfdir}/mdadm.conf
%config(noreplace) %{_sysconfdir}/sysconfig/raid-check
%{_udevrulesdir}/63-md-raid-arrays.rules
%{_udevrulesdir}/64-md-raid-assembly.rules
%{_udevrulesdir}/65-md-incremental.rules
%{_udevrulesdir}/69-md-clustered-confirm-device.rules
%{_udevrulesdir}/01-md-raid-creating.rules
%{_presetdir}/86-%{name}.preset
%{_unitdir}/*.service
%{_unitdir}/*.timer
/lib/systemd/system-shutdown/mdadm.shutdown
%{_tmpfilesdir}/%{name}.conf
%{_sysconfdir}/libreport/events.d/*
%{_mandir}/man*/md*
%{_prefix}/lib/dracut/dracut.conf.d/61-dracut-distro-mdraid.conf
