def validate_blog_form(form: dict) -> str:
    title = form.get('title')
    content = form.get('content')

    if not title:
        return 'Title is required.'
        
    if not content:
        return 'Content is required.'
    
    if len(title) > 100:
        return 'Title must not be more than 100 characters.'
    if len(content) < 80:
        return 'Content must contain at least 80 characters.'
    elif len(content) > 1000:
        return 'Content must not be more than 1000 characters.'