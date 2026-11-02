from zags.defense.mail_report import build_message


def test_mail_counts_failures_errors_and_skips(tmp_path):
    report = tmp_path / "junit.xml"
    report.write_text(
        "<testsuites><testsuite><testcase/>"
        "<testcase><failure/></testcase><testcase><error/></testcase>"
        "<testcase><skipped/></testcase></testsuite></testsuites>"
    )
    message = build_message(report, "https://github.com/example/project/actions/runs/1")
    assert "4 tests, 1 failures, 1 errors" in message["Subject"]
    assert "skipped: 1" in message.get_body().get_content()
    assert len(list(message.iter_attachments())) == 1
