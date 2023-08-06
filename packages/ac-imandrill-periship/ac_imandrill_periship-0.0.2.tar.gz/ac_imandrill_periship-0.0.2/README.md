# Documentation

This is a Mandrill/Transactional Email MailChimp helper function package. 

There are 5 functions available.
* list_all_templates
* template_merge_tags
* send_template
* send_template_attachment
* retrieve_data

----
**Explanation**

*list_all_templates(api_key)* 
> Given a valid API key (string), the function will return a list of 
> template slugs and names.
>
>**Example:**
>
>```
>api_key = "abcd1234567"
>list_of_templates = list_all_templates(api_key)
># list_of_templates could contain:
># [ {'slug': 'example-template', 'name': 'Example Template'} ]
>```

*template_merge_tags(api_key, template_name, merge_language)*
> Given a valid API key (string), template name or slug (string), 
> and specified merge tag language (string), the function will 
> return a list of merge tags in that template. However, there may
> be some merge tags that will be addressed somewhere else. Thus,
> do not need to be defined in global_merge_vars or merge_vars.
>
>**Example:**
>
>```
>api_key = "abcd1234567"
>template_name = "example-template" # can also be "Example Template"
>merge_language = "mailchimp" # or "handlebars"
>list_of_merge_tags = template_merge_tags(api_key, template_name, merge_language)
># list_of_merge_tags could contain:
># {'merge_tags': ['subject', 'fullname', 'activity']}
>```
> 'subject' will be defined somewhere else, so it does not need to be
> defined under global_merge_vars or merge_vars (this is applicable to every 
> template) 

*send_template(api_key, template_name, fields)*
> Given a valid API key (string), template name or slug (string), 
> and fields (struct), the function will return Mandrill's API JSON
> response. 
>
>**Example:**
>
>```
>api_key = "abcd1234567"
>template_name = "example-template" # can also be "Example Template"
>fields = { 
>   'subject': 'This is an example',
>   'from_email': 'example@example.com',
>   'from_name': 'Example Name',
>   'to': [
>       {
>           'email': 'rcpt@example.com',
>           'name': 'Example Rcpt',
>           'type': 'to' #type as is
>       },
>       {
>           'email': 'rcpt2@example.com',
>           'name': 'Example Rcpt2',
>           'type': 'to' #type as is
>       }
>   ],
>   'global_merge_vars': [  
>       {
>           'name': 'merge tag name',
>           'content': 'replace merge tag with'
>       }
>   ],
>   'merge_tags': [ 
>       {
>           'rcpt': 'rcpt2@example.com',
>           'vars': [
>               {
>                   'name': 'merge tag name',
>                   'content': 'replace merge tag content'
>               }
>           ]
>       }
>   ],
>   'merge_language': 'mailchimp'
>}
>
>response = send_template(api_key, template_name, fields)
># response could contain:
># [ 
>#   {'email': 'rcpt@example.com', 'status': 'sent', '_id': '12349853'},
>#   {'email': 'rcpt2@example.com', 'status': 'sent', '_id': '63313685'} 
># ]
>```
> not every attribute is required (ex: just sending generic info to everyone,
> so don't need 'merge_vars')
>
>If the attribute is not needed, you can simply delete it in its entirety.
> 
> 'global_merge_vars' vs 'merge_vars' :: one will replace the merge tags
> with the same info for everyone, and the other will override with specific
> info to a certain recipient (in the case above, Example Rcpt2) 
> 
> 'merge_language' must be either 'mailchimp' or 'handlebars', this just
> depends on what your template is using
> *|MERGETAG|* (mailchimp) or {{*MERGETAG*}} (handlebars)  

*send_template_attachment(api_key, template_name, fields)*
> Similar to *send_template*, but with an additional attribute in 'fields'
>
>**Example:**
>
>```
>api_key = "abcd1234567"
>template_name = "example-template" # can also be "Example Template"
>fields = { 
>   'subject': 'This is an example',
>   'from_email': 'example@example.com',
>   'from_name': 'Example Name',
>   'to': [
>       {
>           'email': 'rcpt@example.com',
>           'name': 'Example Rcpt',
>           'type': 'to' #type as is
>       },
>       {
>           'email': 'rcpt2@example.com',
>           'name': 'Example Rcpt2',
>           'type': 'to' #type as is
>       }
>   ],
>   'global_merge_vars': [  
>       {
>           'name': 'merge tag name',
>           'content': 'replace merge tag with'
>       }
>   ],
>   'merge_tags': [ 
>       {
>           'rcpt': 'rcpt2@example.com',
>           'vars': [
>               {
>                   'name': 'merge tag name',
>                   'content': 'replace merge tag content'
>               }
>           ]
>       }
>   ],
>   'merge_language': 'mailchimp',
>   'attachments': [
>       {
>           'name': 'myfile.txt'
>       },
>       {
>           'name': 'myimage.png'
>       }
>   ]
>}
>
>response = send_template_attachment(api_key, template_name, fields)
># response could contain:
># [ 
>#   {'email': 'rcpt@example.com', 'status': 'sent', '_id': '12349853'},
>#   {'email': 'rcpt2@example.com', 'status': 'sent', '_id': '63313685'} 
># ]
>```
> The same comments from *send_template* apply. If the attribute is not needed, 
> you can simply delete it in its entirety. 
>
> 'attachments' can support any file type, although, images will be sent as
> an attachment, not an embedded image.
>
> This works by using base64 to convert the file into a base64-encoded string,
> which is then sent through Mandrill's API.

*retrieve_data(api_key, query)*
> Given a valid API key (string) and a query (struct), the function returns
> an array of matching messages.
>
>**Example:**
> 
>```
>api_key = "abcd1234567"
>message = {
>   'query': 'rcpt@example.com',
>   'date_from': '2020-06-29',
>   'date_to': '2020-06-30',
>   'tags': [ ]
>   'limit': 100
>}
>matching_msgs = retrieve_data(api_key, messgae)
># matching_msgs could contain:
># [
>#   {
>#      a bunch of fields that Mandrill's API returns per matching message
>#   }
># ]
>```
> none of the attributes in 'message' are required, but they help narrow
> the returned results to messages that are more relevant to what you're
> looking for. Please note how the 'date_from' and 'date_to' strings are
> formatted.
>
> If the attribute is not needed, you can simply delete it in its entirety.
>
[Github-flavored Markdown](https://guides.github.com/features/mastering-markdown/)
