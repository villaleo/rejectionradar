import gmail
import gpt


def main():
    print("fetching recent, unread emails.. ", end="")
    recent_mail, error = gmail.recent_mail()
    if error is not None:
        raise error

    num_msgs = len(recent_mail)
    print(f"done, found {num_msgs} email(s)")
    rejection_email_ids = []

    print("checking for rejections")
    for i, msg in enumerate(recent_mail):
        print(f"{i+1} of {num_msgs}.. ", end="")
        status = gpt.is_rejection(msg)
        if status:
            rejection_email_ids.append(msg["id"])
            print("rejection")
        else:
            print("unknown")

    if not rejection_email_ids:
        print("done, no rejections detected")
        return

    LABEL = "Rejections"
    print(f"applying label {LABEL} to {len(rejection_email_ids)} email(s)..", end="")
    label_id, error = gmail.get_label_id(LABEL)
    if error is not None:
        raise error

    if not label_id:
        id, error = gmail.create_label(LABEL)
        if error is not None:
            raise error
        label_id = str(id)

    error = gmail.apply_label(label_id, rejection_email_ids)
    if error is not None:
        raise error
    print("done")


if __name__ == "__main__":
    main()
