from wagtail_tag_manager.settings import StaticFilesSettings


def export_static_files_settings(request):
    return {
        "WTM_INCLUDE_CSS": StaticFilesSettings.include_css,
        "WTM_INCLUDE_JS": StaticFilesSettings.include_js,
    }
