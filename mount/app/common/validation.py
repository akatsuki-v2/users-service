import email_validator


def validate_email(email: str) -> bool:
    try:
        # TODO: asynchronize the deliverability checks?
        email_validator.validate_email(email)
    except email_validator.EmailNotValidError as e:
        return False
    else:
        return True
