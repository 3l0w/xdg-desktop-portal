env_tests = environment()
env_tests.set('XDP_UNINSTALLED', '1')
env_tests.set('XDG_DATA_DIRS', meson.current_build_dir() / 'share')
env_tests.set('XDP_VALIDATE_ICON', xdp_validate_icon.full_path())
env_tests.set('XDP_VALIDATE_SOUND', xdp_validate_sound.full_path())
env_tests.set('G_TEST_SRCDIR', meson.current_source_dir())
env_tests.set('G_TEST_BUILDDIR', meson.current_build_dir())
env_tests.set('G_DEBUG', 'gc-friendly')  # from glib-tap.mk
env_tests.set('LSAN_OPTIONS', 'suppressions=' + meson.current_source_dir() / 'asan.suppression')

if glib_dep.version().version_compare('>= 2.68')
  test_protocol = 'tap'
else
  test_protocol = 'exitcode'
endif

subdir('dbs')
subdir('portals')
subdir('services')
subdir('share')

test_db = executable(
  'testdb',
  ['testdb.c'] + db_sources,
  dependencies: [common_deps],
  include_directories: [common_includes],
  install: enable_installed_tests,
  install_dir: installed_tests_dir,
)
test(
  'testdb',
  test_db,
  env: env_tests,
  is_parallel: false,
  protocol: test_protocol,
)

if enable_installed_tests
  install_data('dbs/no_tables', install_dir: installed_tests_dir / 'dbs')
endif

test_doc_portal = executable(
  'test-doc-portal',
  'can-use-fuse.c',
  'test-doc-portal.c',
  'utils.c',
  document_portal_built_sources,
  dependencies: [common_deps, fuse3_dep],
  include_directories: [common_includes],
  install: enable_installed_tests,
  install_dir: installed_tests_dir,
)
test(
  'test-doc-portal',
  test_doc_portal,
  env: env_tests,
  is_parallel: false,
  protocol: test_protocol,
)

# We build this in the tests/ subdirectory so that it can be accessed
# via G_TEST_BUILT
test_backends = executable(
  'test-backends',
  'backend/test-backends.c',
  'backend/access.c',
  'backend/account.c',
  'backend/appchooser.c',
  'backend/background.c',
  'backend/email.c',
  'backend/filechooser.c',
  'backend/inhibit.c',
  'backend/lockdown.c',
  'backend/notification.c',
  'backend/print.c',
  'backend/screenshot.c',
  'backend/settings.c',
  'backend/wallpaper.c',
  'backend/xdp-request.c',
  'backend/xdp-session.c',
  'glib-backports.c',
  document_portal_built_sources,
  document_portal_built_sources,
  impl_built_sources,
  dependencies: [common_deps],
  include_directories: [common_includes, src_includes],
  install: enable_installed_tests,
  install_dir: installed_tests_dir,
)

portals_test_deps = []
portals_test_sources = files()

if have_libportal
  portals_test_deps += [libportal_dep]

  portals_test_sources += files(
    'account.c',
    'background.c',
    'camera.c',
    'email.c',
    'filechooser.c',
    'inhibit.c',
    'notification.c',
    'openuri.c',
    'print.c',
    'screenshot.c',
    'trash.c',
    'wallpaper.c',
    'glib-backports.c',
  )
endif

test_portals = executable(
  'test-portals',
  'test-portals.c',
  'utils.c',
  portals_test_sources,
  impl_built_sources,
  permission_store_built_sources,
  portal_built_sources,
  xdp_utils_sources,
  dependencies: [common_deps, portals_test_deps, xdp_utils_deps],
  include_directories: [common_includes, xdp_utils_includes],
  c_args: [
    '-DXDG_DP_BUILDDIR="src"',
    '-DXDG_PS_BUILDDIR="document-portal"',
  ],
  install: enable_installed_tests,
  install_dir: installed_tests_dir,
)

limited_portals = executable(
  'limited-portals',
  'limited-portals.c',
  'utils.c',
  portals_test_sources,
  impl_built_sources,
  permission_store_built_sources,
  portal_built_sources,
  xdp_utils_sources,
  dependencies: [common_deps, portals_test_deps, xdp_utils_deps],
  include_directories: [common_includes, xdp_utils_includes],
  c_args: [
    '-DXDG_DP_BUILDDIR="src"',
    '-DXDG_PS_BUILDDIR="document-portal"',
  ],
  install: enable_installed_tests,
  install_dir: installed_tests_dir,
)

# Split the portal tests into one test per portal, this makes debugging a lot
# easier.
# Keep in sync with test-portals.c
portal_tests = [
  'account',
  'background',
  'camera',
  'color',
  'email',
  'inhibit',
  'notification',
  'openfile',
  'openuri',
  'prepareprint',
  'print',
  'savefile',
  'screenshot',
  'settings',
  'trash',
  'wallpaper',
]

test_env = env_tests
test_env.set('XDG_CURRENT_DESKTOP', 'test')
foreach p : portal_tests
    test(
      'test-portals-@0@'.format(p),
      test_portals,
      args: ['--verbose', '--keep-going', '--tap', '-p', '/portal/@0@'.format(p)],
      depends: [test_backends, test_portals],
      env: test_env,
      protocol: test_protocol,
      suite: 'portals',
    )
endforeach

# Split the portal tests into one test per portal, this makes debugging a lot
# easier.
# Keep in sync with test-portals.c
portal_limited = [
  'openfile',
  'savefile',
]

limited_env = env_tests
limited_env.set('XDG_CURRENT_DESKTOP', 'limited')
foreach p : portal_limited
    test(
      'limited-portals-@0@'.format(p),
      limited_portals,
      args: ['--verbose', '--keep-going', '--tap', '-p', '/limited/@0@'.format(p)],
      depends: [test_backends, limited_portals],
      env: limited_env,
      protocol: test_protocol,
      suite: 'portals',
    )
endforeach

test_permission_store = executable(
  'test-permission-store',
  'test-permission-store.c',
  'utils.c',
  permission_store_built_sources,
  xdp_utils_sources,
  dependencies: [common_deps, xdp_utils_deps],
  include_directories: [common_includes, xdp_utils_includes],
  install: enable_installed_tests,
  install_dir: installed_tests_dir,
)
test(
  'test-permission-store',
  test_permission_store,
  env: env_tests,
  is_parallel: false,
  protocol: test_protocol,
)

test_xdp_utils = executable(
  'test-xdp-utils',
  'test-xdp-utils.c',
  'utils.c',
  xdp_utils_sources,
  dependencies: [common_deps, xdp_utils_deps],
  include_directories: [common_includes, xdp_utils_includes],
  install: enable_installed_tests,
  install_dir: installed_tests_dir,
)
test(
  'test-xdp-utils',
  test_xdp_utils,
  env: env_tests,
  is_parallel: false,
  protocol: test_protocol,
)

test_method_info = executable(
  'test-xdp-method-info',
  'test-xdp-method-info.c',
  xdp_method_info_sources,
  dependencies: [common_deps],
  include_directories: [common_includes, xdp_utils_includes],
  install: enable_installed_tests,
  install_dir: installed_tests_dir,
)
test(
  'test-xdp-method-info',
  test_method_info,
  env: env_tests,
  is_parallel: true,
  protocol: test_protocol,
)

pytest = find_program('pytest-3', 'pytest', required: get_option('pytest'))
python = pymod.find_installation(
  'python3',
  modules: ['dbus', 'dbusmock', 'gi'],
  required: get_option('pytest'),
)

enable_pytest = get_option('pytest') \
  .require(pytest.found()) \
  .require(python.found() and python.language_version().version_compare('>=3.9'),
           error_message: 'Python version >=3.9 is required') \
  .require(umockdev_dep.found()) \
  .require(have_wav_parse,
           error_message: 'gst-inspect and the wavparse plugins are required') \
  .allowed()

if enable_pytest
  pytest_args = ['--verbose', '--log-level=DEBUG']

  pytest_env = environment()
  pytest_env.set('XDG_DESKTOP_PORTAL_PATH', xdg_desktop_portal.full_path())
  pytest_env.set('XDG_PERMISSION_STORE_PATH', xdg_permission_store.full_path())
  pytest_env.set('XDG_DOCUMENT_PORTAL_PATH', xdg_document_portal.full_path())
  pytest_env.set('XDP_VALIDATE_ICON', xdp_validate_icon.full_path())
  pytest_env.set('XDP_VALIDATE_SOUND', xdp_validate_sound.full_path())

  # pytest xdist is nice because it significantly speeds up our
  # test process, but it's not required
  if pymod.find_installation('python3', modules: ['xdist'], required: false).found()
    # using auto can easily start too many tests which will block each other
    # a value of around 5 seems to work well
    pytest_args += ['-n', '5']
  endif

  pytest_files = [
    'test_account.py',
    'test_background.py',
    'test_camera.py',
    'test_clipboard.py',
    'test_documents.py',
    'test_document_fuse.py',
    'test_dynamiclauncher.py',
    'test_email.py',
    'test_filechooser.py',
    'test_globalshortcuts.py',
    'test_inhibit.py',
    'test_inputcapture.py',
    'test_location.py',
    'test_notification.py',
    'test_openuri.py',
    'test_permission_store.py',
    'test_print.py',
    'test_registry.py',
    'test_remotedesktop.py',
    'test_settings.py',
    'test_screenshot.py',
    'test_trash.py',
    'test_usb.py',
    'test_wallpaper.py',
  ]

  template_files = [
    'templates/access.py',
    'templates/account.py',
    'templates/appchooser.py',
    'templates/background.py',
    'templates/clipboard.py',
    'templates/dynamiclauncher.py',
    'templates/email.py',
    'templates/filechooser.py',
    'templates/geoclue2.py',
    'templates/globalshortcuts.py',
    'templates/inhibit.py',
    'templates/__init__.py',
    'templates/inputcapture.py',
    'templates/lockdown.py',
    'templates/notification.py',
    'templates/print.py',
    'templates/remotedesktop.py',
    'templates/screenshot.py',
    'templates/settings.py',
    'templates/usb.py',
    'templates/wallpaper.py',
  ]

  foreach pytest_file : pytest_files
    testname = pytest_file.replace('.py', '')
    test(
      'pytest/@0@'.format(testname),
      pytest,
      args: [meson.current_source_dir() / pytest_file] + pytest_args,
      env: pytest_env,
      suite: ['pytest'],
      timeout: 120,
    )
  endforeach

  if enable_installed_tests
    install_data(
      pytest_files,
      '__init__.py',
      'conftest.py',
      'asan.suppression',
      install_dir: installed_tests_dir / 'tests',
    )
    install_data(
      template_files,
      install_dir: installed_tests_dir / 'tests' / 'templates',
    )

    installed_env = {
      'XDG_DESKTOP_PORTAL_PATH': libexecdir / 'xdg-desktop-portal',
      'XDG_PERMISSION_STORE_PATH': libexecdir / 'xdg-permission-store',
      'XDG_DOCUMENT_PORTAL_PATH': libexecdir / 'xdg-document-portal',
      'XDP_VALIDATE_AUTO': '1',
    }
    env = ''
    foreach key, value : installed_env
      env += f'@key@=@value@ '
    endforeach

    foreach pytest_file : pytest_files
      testname = pytest_file.replace('.py', '')

      exec = [pytest.full_path(), installed_tests_dir / 'tests' / pytest_file]
      exec += pytest_args
      exec += ['-p', 'no:cacheprovider']
      exec = ' '.join(exec)

      data = configuration_data()
      data.set('exec', exec)
      data.set('env', env)
      data.set('libdir', libdir)

      configure_file(
        input: 'template.test.in',
        output: '@0@.test'.format(testname),
        configuration: data,
        install: true,
        install_dir: installed_tests_data_dir,
      )
    endforeach
  endif
endif

if enable_installed_tests
  # autotools used to symlink to the host files, here we just install our version
  install_data(
    doc_portal_service_file,
    permission_portal_service_file,
    install_dir: installed_tests_dir / 'services',
  )

  installed_tests_env = 'XDG_DATA_DIRS=@0@/share:@1@:/usr/local/share:/usr/share'
  installed_tests_env = installed_tests_env.format(installed_tests_data_dir, datadir)

  testfiles = [
    'testdb',
    'test-doc-portal',
    'test-permission-store',
    'test-xdp-utils',
  ]
  foreach tf : testfiles
      data = configuration_data()
      data.set('exec', installed_tests_dir / tf)
      data.set('env', installed_tests_env)
      data.set('libdir', libdir)
      configure_file(
        input: 'template-tap.test.in',
        output: '@0@.test'.format(tf),
        configuration: data,
        install: true,
        install_dir: installed_tests_data_dir,
      )
  endforeach

  foreach p : portal_tests
      data = configuration_data()
      data.set('exec', '@0@ -p /portal/@1@'.format(installed_tests_dir / 'test-portals', p))
      data.set('env', installed_tests_env)
      data.set('libdir', libdir)
      configure_file(
        input: 'template-tap.test.in',
        output: 'test-portals-@0@.test'.format(p),
        configuration: data,
        install: true,
        install_dir: installed_tests_data_dir,
      )
  endforeach

  foreach p : portal_limited
      data = configuration_data()
      data.set('exec', '@0@ -p /limited/@1@'.format(installed_tests_dir / 'limited-portals', p))
      data.set('env', installed_tests_env)
      data.set('libdir', libdir)
      configure_file(
        input: 'template-tap.test.in',
        output: 'test-limited-@0@.test'.format(p),
        configuration: data,
        install: true,
        install_dir: installed_tests_data_dir,
      )
  endforeach
endif

meson.add_devenv(test_env)
