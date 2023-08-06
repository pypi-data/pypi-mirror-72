import base64
import mandrill
import re


def list_all_templates(api_key):
    m_client = mandrill.Mandrill(api_key)
    temp_list = m_client.templates.list()
    ret_list = []
    for en in temp_list:
        entry = {'slug': en['slug'], 'name': en['name']}
        ret_list.append(entry)
    return ret_list


def template_merge_tags(api_key, template_name, merge_language):
    m_client = mandrill.Mandrill(api_key)
    info = m_client.templates.info(template_name)
    subject_line = info['subject']
    code = info['code']
    if merge_language == 'mailchimp':
        all_merge_tags = re.findall('\*\|(.*?)\|\*', code)
        add_merge_tags = re.findall('\*\|(.*?)\|\*', subject_line)
    elif merge_language == 'handlebars':
        all_merge_tags = re.findall('\{\{(.*?)\}\}', code)
        add_merge_tags = re.findall('\{\{(.*?)\}\}', subject_line)
    else:
        return "Invalid merge_language: supports mailchimp or handlebars"
    merge_tags = []
    for tag in all_merge_tags:
        if ':' not in tag and 'MC' not in tag:
            merge_tags.append(tag.lower())
    for tag in add_merge_tags:
        if tag.lower() not in merge_tags:
            merge_tags.append(tag.lower())
    return {'merge_tags': merge_tags}


def send_template(api_key, template_name, fields):
    # callers need to provide:
    # subject, from_email, to[], merge_vars[], merge_tag_language, bcc_address
    try:
        m_client = mandrill.Mandrill(api_key)
        msg_to_send = {
            "subject": fields['subject'] if 'subject' in fields.keys() else None,
            "from_email": fields['from_email'],
            "from_name": fields['from_name'] if 'from_name' in fields.keys() else None,
            "to": fields['to'],
            "important": True,
            "track_opens": True,
            "track_clicks": True,
            "auto_text": None,
            "auto_html": None,
            "inline_css": None,
            "url_strip_qs": None,
            "preserve_recipients": None,
            "view_content_link": None,
            "bcc_address": fields['bcc_address'] if 'bcc_address' in fields.keys() else None,
            "tracking_domain": None,
            "signing_domain": None,
            "return_path_domain": None,
            "merge": True if 'merge_vars' in fields.keys() or 'global_merge_vars' in fields.keys() else False,
            "merge_language": fields['merge_language'] if 'merge_language' in fields.keys() else None,
            "global_merge_vars": fields['global_merge_vars'] if 'global_merge_vars' in fields.keys() else None,
            "merge_vars": fields['merge_vars'] if 'merge_vars' in fields.keys() else None,
            "tags": fields['tags'] if 'tags' in fields.keys() else None,
            "subaccount": None,
            "google_analytics_domains": None,
            "metadata": None,
            "recipient_metadata": None,
            "attachments": None,
            "images": None
        }
        return m_client.messages.send_template(template_name, [], msg_to_send)
    except KeyError:
        return "Missing required field in message="


def image_to_base64_encoder(image_path):
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode('utf-8')


def send_template_attachment(api_key, template_name, fields):
    # callers need to provide:
    # subject, from_email, to[], merge_vars[], merge_tag_language, bcc_address
    try:
        attachment_list = fields['attachments']
        structured_attachments = []
        for attach in attachment_list:
            entry = {'type': 'application/octet-stream', 'name': attach['name'],
                     'content': image_to_base64_encoder(attach['name'])}
            structured_attachments.append(entry)
        m_client = mandrill.Mandrill(api_key)
        msg_to_send = {
            "subject": fields['subject'] if 'subject' in fields.keys() else None,
            "from_email": fields['from_email'],
            "from_name": fields['from_name'] if 'from_name' in fields.keys() else None,
            "to": fields['to'],
            "important": True,
            "track_opens": True,
            "track_clicks": True,
            "auto_text": None,
            "auto_html": None,
            "inline_css": None,
            "url_strip_qs": None,
            "preserve_recipients": None,
            "view_content_link": None,
            "bcc_address": fields['bcc_address'] if 'bcc_address' in fields.keys() else None,
            "tracking_domain": None,
            "signing_domain": None,
            "return_path_domain": None,
            "merge": True if 'merge_vars' in fields.keys() or 'global_merge_vars' in fields.keys() else False,
            "merge_language": fields['merge_language'] if 'merge_language' in fields.keys() else None,
            "global_merge_vars": fields['global_merge_vars'] if 'global_merge_vars' in fields.keys() else None,
            "merge_vars": fields['merge_vars'] if 'merge_vars' in fields.keys() else None,
            "tags": fields['tags'] if 'tags' in fields.keys() else None,
            "subaccount": None,
            "google_analytics_domains": None,
            "metadata": None,
            "recipient_metadata": None,
            "attachments": structured_attachments,
            "images": None
        }
        return m_client.messages.send_template(template_name, [], msg_to_send)
    except KeyError:
        return "Missing required field in message="


def retrieve_data(api_key, query):
    # query = {query, date_to, date_from, tags, limit}
    m_client = mandrill.Mandrill(api_key)
    if len(query.keys()) == 0:
        return "Missing required field in query="
    return m_client.messages.search(query=query['query'],
                                    date_to=query['date_to'] if 'date_to' in query.keys() else None,
                                    date_from=query['date_from'] if 'date_from' in query.keys() else None,
                                    tags=query['tags'] if 'tags' in query.keys() else None,
                                    limit=query['limit'] if 'limit' in query.keys() else None)
