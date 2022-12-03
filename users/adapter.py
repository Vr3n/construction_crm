from allauth.account.adapter import DefaultAccountAdapter

# Create your adapter here.


class GCAccountAdapter(DefaultAccountAdapter):
    def render_mail(self, template_prefix, email, context):
        """
        Renders an e-mail to `email`.  `template_prefix` identifies the
        e-mail that is to be sent, e.g. "account/email/email_confirmation"
        """
        to = [email] if isinstance(email, str) else email
        subject = render_to_string(
            "{0}_subject.txt".format(template_prefix), context)
        # remove superfluous line breaks
        subject = " ".join(subject.splitlines()).strip()
        subject = self.format_email_subject(subject)

        from_email = self.get_from_email()

        bodies = {}
        for ext in ["html"]:
            try:
                template_name = "{0}_message.{1}".format(template_prefix, ext)
                bodies[ext] = render_to_string(
                    template_name,
                    context,
                    self.request,
                ).strip()
            except TemplateDoesNotExist:
                if ext == "html" and not bodies:
                    # We need at least one body
                    raise
            msg = EmailMessage(subject, bodies["html"], from_email, to)
            msg.content_subtype = "html"  # Main content is now text/html
        return msg

    def send_mail(self, template_prefix, email, context):
        msg = self.render_mail(template_prefix, email, context)
        msg.send()