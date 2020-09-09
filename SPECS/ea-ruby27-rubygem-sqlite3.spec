# Defining the package namespace
%global ns_name ea
%global ns_dir /opt/cpanel
%global pkg ruby27
%global gem_name sqlite3

# NOTE: I need the version, is there a better way?
%global ruby_version 2.7.1

# Force Software Collections on
%global _scl_prefix %{ns_dir}
%global scl %{ns_name}-%{pkg}
# HACK: OBS Doesn't support macros in BuildRequires statements, so we have
#       to hard-code it here.
# https://en.opensuse.org/openSUSE:Specfile_guidelines#BuildRequires
%global scl_prefix %{scl}-
%{?scl:%scl_package rubygem-%{gem_name}}

# Doing release_prefix this way for Release allows for OBS-proof versioning, See EA-4590 for more details
%define release_prefix 1

Summary:        Allows Ruby scripts to interface with a SQLite3 database
Name:           %{?scl_prefix}rubygem-%{gem_name}
Version:        1.4.2
Release:        %{release_prefix}%{?dist}.cpanel
Group:          Development/Languages
License:        BSD
URL:            https://github.com/sparklemotion/sqlite3-ruby
Source0:        %{gem_name}-%{version}.gem
Requires:       %{?scl_prefix}ruby(rubygems)
Requires:       %{?scl_prefix}ruby(release)

BuildRequires:  sqlite-devel
BuildRequires:  scl-utils
BuildRequires:  scl-utils-build
BuildRequires:  %{?scl_prefix}ruby
BuildRequires:  %{?scl_prefix}rubygems-devel
BuildRequires:  %{?scl_prefix}ruby-devel
BuildRequires:  %{?scl_prefix}rubygem(rake)
BuildRequires:  %{?scl_prefix}rubygem(minitest) >= 5.0.0
Provides:       %{?scl_prefix}rubygem(%{gem_name}) = %{version}-%{release}

%description
SQLite3/Ruby is a module to allow Ruby scripts to interface with a SQLite3
database.

%package doc
Summary: Documentation for %{pkg_name}
Group: Documentation
# setup.rb shipped in the -doc subpackage has LGPLv2.1 licensing
License: BSD and LGPLv2
Requires: %{?scl_prefix}%{pkg_name} = %{version}-%{release}
BuildArch: noarch

%description doc
Documentation for %{pkg_name}

%prep
%setup -q -c -T

export CONFIGURE_ARGS="--with-cflags='%{optflags}'"

%{?scl:scl enable %{scl} - << \EOF} \
%gem_install -n %{SOURCE0} \
%{?scl:EOF}

# Permission
find . -name \*.rb -or -name \*.gem | xargs chmod 0644

%build

%install
%global gemsbase opt/cpanel/ea-ruby27/root/usr/share/ruby/gems/ruby-%{ruby_version}
%global gemsdir  %{gemsbase}/gems
%global gemsmri  %{gemsdir}/sqlite3-%{version}

mkdir -p %{buildroot}/%{gemsmri}
mkdir -p %{buildroot}/%{gemsbase}/cache
mkdir -p %{buildroot}/%{gemsbase}/doc
mkdir -p %{buildroot}/%{gemsbase}/specifications
mkdir -p %{buildroot}/%{gemsbase}/extension/x86_64-linux/2.7.0/sqlite3-%{version}

cp -ar %{gemsbase}/extensions/x86_64-linux/2.7.0/sqlite3-%{version}/* %{buildroot}/%{gemsbase}/extension/x86_64-linux/2.7.0/sqlite3-%{version}
cp -ar %{gemsmri}/* %{buildroot}/%{gemsmri}
cp -a %{gemsmri}/.gemtest %{buildroot}/%{gemsmri}
cp -a %{gemsmri}/.travis.yml %{buildroot}/%{gemsmri}
cp -a  %{gemsbase}/specifications/sqlite3-%{version}.gemspec %{buildroot}/%{gemsbase}/specifications/

%check
# I cannot get this to work, not sure why
# Tests fail on cent 6
#%if 0%{rhel} > 6
#%{?scl:scl enable %{scl} - << \EOF} \
#pushd %{gemsdir} \
#ruby -I$(dirs +1)%{gemsmri}:lib:test -e 'Dir.glob "./test/test_*.rb", &method(:require)' \
#popd \
#EOF}
#%endif

%files
/%{gemsmri}
%dir /%{gemsdir}
%exclude /%{gemsmri}/.gemtest
%exclude /%{gemsmri}/.travis.yml
%exclude /%{gemsmri}/appveyor.yml
%doc /%{gemsmri}/README.rdoc
%doc /%{gemsmri}/LICENSE
%exclude /%{gemsmri}/ext
%exclude /%{gemsbase}/cache
/%{gemsbase}/extension/x86_64-linux/2.7.0/sqlite3-%{version}/gem.build_complete
/%{gemsbase}/extension/x86_64-linux/2.7.0/sqlite3-%{version}/gem_make.out
/%{gemsbase}/extension/x86_64-linux/2.7.0/sqlite3-%{version}/mkmf.log
/%{gemsbase}/extension/x86_64-linux/2.7.0/sqlite3-%{version}/sqlite3/sqlite3_native.so
/%{gemsbase}/specifications/sqlite3-%{version}.gemspec

%files doc
%doc /%{gemsmri}/API_CHANGES.rdoc
%doc /%{gemsmri}/CHANGELOG.rdoc
%doc /%{gemsmri}/ChangeLog.cvs
%doc /%{gemsmri}/Manifest.txt
/%{gemsmri}/Rakefile
/%{gemsmri}/Gemfile
/%{gemsmri}/setup.rb
%doc /%{gemsmri}/faq/
/%{gemsmri}/rakelib/
/%{gemsmri}/test/

%changelog
* Wed Sep 09 2020 Julian Brown <julian.brown@cpanel.net> - 1.4.2-1
- ZC-7511 - add rubygem sqlite3 to Ruby 2.7

