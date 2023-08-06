"""
Helper functions for sending a notification email after each deployment.
"""
from __future__ import print_function

import smtplib
from email.mime.text import MIMEText

from burlap import Satchel
from burlap.constants import *
from burlap.decorators import task

PRE_DEPLOYMENT = 'pre'
POST_DEPLOYMENT = 'post'
FAILED_DEPLOYMENT = 'failed'


class DeploymentNotifierSatchel(Satchel):

    name = 'deploymentnotifier'

    def set_defaults(self):

        self.env.email_enabled = False
        self.env.email_host = None
        self.env.email_port = 587
        self.env.email_host_user = None
        self.env.email_host_password = None
        self.env.email_use_tls = True
        self.env.email_recipient_list = []

    def send_email(self, subject, message, from_email=None, recipient_list=None):

        recipient_list = recipient_list or []
        if not recipient_list:
            return

        from_email = from_email or self.env.email_host_user

        msg = MIMEText(message)

        # me == the sender's email address
        # you == the recipient's email address
        msg['Subject'] = subject
        msg['From'] = from_email
        msg['To'] = '; '.join(recipient_list)

        # Send the message via our own SMTP server, but don't include the
        # envelope header.
        print('Attempting to send mail using %s@%s...' \
            % (self.env.email_host_user, self.env.email_host))
        s = smtplib.SMTP(self.env.email_host, self.env.email_port)
        s.ehlo()
        s.starttls()
        s.ehlo()
        self.vprint('user:', self.env.email_host_user, 'password:', self.env.email_host_password)
        s.login(self.env.email_host_user, self.env.email_host_password)
        s.sendmail(from_email, recipient_list, msg.as_string())
        s.quit()

    @task
    def test(self):
        self.send_email(
            subject='Test',
            message='Test',
            recipient_list=self.env.email_recipient_list)

    def notify_deployment(self, action, subject=None, message=None, force=0):
        """
        Send email notifying recipients of deploy start, completion, or failure.
        """
        force = int(force)

        if not subject:
            subject = {
                PRE_DEPLOYMENT: '%s Deployment Started' % self.genv.ROLE.title(),
                POST_DEPLOYMENT: '%s Deployment Complete' % self.genv.ROLE.title(),
                FAILED_DEPLOYMENT: '%s Deployment Failed' % self.genv.ROLE.title(),
            }[action]

        if not message:
            message = {
                PRE_DEPLOYMENT: 'Deployment to %s has started.' % self.genv.ROLE,
                POST_DEPLOYMENT: 'Deployment to %s is complete.' % self.genv.ROLE,
                FAILED_DEPLOYMENT: 'Deployment to %s has failed.' % self.genv.ROLE,
            }[action]


        if self.dryrun:
            self.print_command('echo -e "{body}" | mail -s "{subject}" {recipients}'.format(
                recipients=','.join(self.env.email_recipient_list),
                body=message.replace('\n', '\\n'),
                subject=subject,
            ))
        elif force or self.env.email_enabled and (
            action == FAILED_DEPLOYMENT
            or action == PRE_DEPLOYMENT and self.genv.host_string == self.genv.hosts[0]
            or action == POST_DEPLOYMENT and self.genv.host_string == self.genv.hosts[-1]
        ):
            self.send_email(
                subject=subject,
                message=message,
                recipient_list=self.env.email_recipient_list)

    @task
    def notify_pre_deployment(self, subject=None, message=None, force=0):
        self.notify_deployment(action=PRE_DEPLOYMENT, subject=subject, message=message, force=force)

    @task
    def notify_post_deployment(self, subject=None, message=None, force=0):
        self.notify_deployment(action=POST_DEPLOYMENT, subject=subject, message=message, force=force)

    @task
    def notify_failed_deployment(self, subject=None, message=None, force=0):
        self.notify_deployment(action=FAILED_DEPLOYMENT, subject=subject, message=message, force=force)

    @task
    def configure(self):
        pass


class LoginNotifierSatchel(Satchel):
    """
    Causes a notification email to be sent whenever someone logs into the server.

    The mail functionality setup by this satchel is pretty light, and generally assumes your server hasn't been blacklisted for spamming.

    If you require a specific SMTP login to send email, then you might have to enable the postfix satchel as well.
    """

    name = 'loginnotifier'

    def set_defaults(self):
        self.env.sysadmin_email = 'root@localhost'
        self.env.script_template = 'notifier/loginnotifier.template.sh'
        self.env.script_installation_path = '/etc/profile.d/loginnotifier.sh'
        self.env.script_user = 'root'
        self.env.script_group = 'root'
        self.env.script_chmod = 'u+rx,g+rx'
        self.env.append_bash_aliases = False

    @property
    def packager_system_packages(self):
        return {
            UBUNTU: [
                # 'postfix',
                'mailutils',
                # 'libsasl2-2',
                # 'ca-certificates',
                # 'libsasl2-modules',
                # 'nano',
            ],
        }

    @task(precursors=['packager', 'user'])
    def configure(self):
        r = self.local_renderer
        if self.env.enabled:
            fn = self.render_to_file(self.env.script_template)
            r.put(
                local_path=fn,
                remote_path=self.env.script_installation_path, use_sudo=True)
            r.sudo('chown {script_user}:{script_group} {script_installation_path}')
            r.sudo('chmod {script_chmod} {script_installation_path}')
        else:
            r.sudo('rm {script_installation_path}')

        if r.env.append_bash_aliases:
            r.append(text='bash %s' % r.env.script_installation_path, filename='~/.bash_aliases')


deployment_notifier = DeploymentNotifierSatchel()
notify_pre_deployment = deployment_notifier.notify_pre_deployment
notify_post_deployment = deployment_notifier.notify_post_deployment
notify_failed_deployment = deployment_notifier.notify_failed_deployment
send_email = deployment_notifier.send_email

login_notifier = LoginNotifierSatchel()
