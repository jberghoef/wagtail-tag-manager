from wagtail_tag_manager.settings import StaticFilesSettings


def export_static_files_settings(request):
    return {
        "WMT_INCLUDE_CSS": StaticFilesSettings.include_css,
        "WMT_INCLUDE_JS": StaticFilesSettings.include_js,
    }
