def validate_blog_form(form: dict) -> str:
    title = form.get('title')
    content = form.get('content')

    if not title:
        return 'Title is required.'
        
    if not content:
        return 'Content is required.'