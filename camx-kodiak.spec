%global debug_package %{nil}
%global __os_install_post %{nil}
%global _build_id_links none

%global camx_platform    kodiak
%global camx_basedir     %{_prefix}/lib
%global camx_plugin_dir  %{camx_basedir}/camx/%{camx_platform}
%global camx_hexagon_dsp_dir %{_datadir}/hexagon-dsp/qcm6490/Thundercomm/RB3gen2/dsp/cdsp

%global upstream_tag 260831

%global __provides_exclude_from ^(%{camx_plugin_dir}|%{_datadir}/qcom|%{camx_hexagon_dsp_dir})/.*$
%global __requires_exclude ^lib(adsp_.*|bitml_nsp.*|bitmlenginev2|camera_hardware|camera_metadata|camera_nn_stub|camx_hardware|camx_metadata|camxcommonutils|camxexternalformatutils|camxfdengine|camxgenerated|camximageformatutils|camxifestriping|camxsensorconfig|camxtintlessalgo|chicustomization|chilog|chiofflinepostproclib|com\\.qti\\.camx\\.chiiqutils|com\\.qti\\.chinodeutils|defog|dsp_streamer.*|ipebpsstriping|ipebpsstriping170|offlinedump|shdr3|swregistrationalgo)\\.so.*$

Name:           camx-kodiak
Version:        1.0.39
Release:        1%{?dist}
Summary:        Qualcomm CamX camera driver libraries for Kodiak (QCM6490)

License:        LicenseRef-Qualcomm-Proprietary
URL:            http://support.cdmatech.com

Source0:        https://qartifactory-edge.qualcomm.com/artifactory/qsc_releases/software/chip/component/camx.qclinux.0.0/%{upstream_tag}/prebuilt_el10/%{name}-%{version}_%{release}.aarch64.tar.gz

ExclusiveArch:  aarch64

Recommends:     qcom-adreno-cl
Recommends:     qcom-adreno-egl
Recommends:     qcom-adreno-gles2

%description
Qualcomm CamX usermode libraries for the Kodiak (QCM6490) platform.

Core camera driver components: the CamX HAL3 module, the CHI feature and node
plugin set, per-sensor tuning data, and the nativehaltest bring-up utility.
Repackaged unchanged from Stage 1's build output; contains no source.

%package -n libcamx-kodiak1
Summary:        Qualcomm CamX libraries for camera service
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description -n libcamx-kodiak1
Set of libraries used by the camera service (QMMF) on the Kodiak platform.

These are the _kodiak-suffixed siblings of the plugin-private libraries: QMMF
links libcamx_hardware_kodiak / libcamx_metadata_kodiak from /usr/lib, whereas
nativehaltest uses the unsuffixed pair inside the private plugin directory. A
GStreamer/QMMF camera path needs this package; a nativehaltest-only bring-up
does not.

%package -n libcamx-kodiak-devel
Summary:        Development files for the CamX camera service libraries
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       libcamx-kodiak1%{?_isa} = %{version}-%{release}

%description -n libcamx-kodiak-devel
Unversioned .so linker symlinks for the CamX camera service (QMMF) libraries
on the Kodiak platform.

Symlinks only -- no headers. The consumer-facing CamX headers are packaged
separately as libcamx-dev from the target-agnostic headers tarball.

%prep
%setup -q -n %{name}-%{version}

%build

%install
cp -a usr %{buildroot}/

rm -rf %{buildroot}%{_includedir}/camx-v1
rm -rf %{buildroot}%{_includedir}/camx
rm -rf %{buildroot}%{_includedir}/autogen
rm -rf %{buildroot}%{_defaultlicensedir}/libcamx-dev
rm -rf %{buildroot}%{_defaultlicensedir}/camx-kodiak-devel
rm -rf %{buildroot}%{_docdir}/libcamx-dev
rm -rf %{buildroot}%{_docdir}/camx-kodiak-devel

%files
%dir %{_defaultlicensedir}/%{name}
%license %{_defaultlicensedir}/%{name}/LICENSE.qcom-2
%doc %{_docdir}/%{name}/NOTICE

%{camx_basedir}/camx

%dir %{_libexecdir}/%{name}
%{_libexecdir}/%{name}/nativehaltest

%dir %{_datadir}/camx
%{_datadir}/camx/*.bin

%{camx_hexagon_dsp_dir}/*.so

%files -n libcamx-kodiak1
%dir %{_defaultlicensedir}/libcamx-kodiak1
%license %{_defaultlicensedir}/libcamx-kodiak1/LICENSE.qcom-2
%doc %{_docdir}/libcamx-kodiak1/NOTICE
%{camx_basedir}/lib*_kodiak.so.*

%files -n libcamx-kodiak-devel
%dir %{_defaultlicensedir}/libcamx-kodiak-devel
%license %{_defaultlicensedir}/libcamx-kodiak-devel/LICENSE.qcom-2
%doc %{_docdir}/libcamx-kodiak-devel/NOTICE
%{camx_basedir}/lib*_kodiak.so

%changelog
* Thu Sep 10 2026 Kripalsinh Rana <kripalsi@qti.qualcomm.com> - 1.0.39-1
- Initial RPM packaging-only release for the prebuilt Kodiak CamX payload.
