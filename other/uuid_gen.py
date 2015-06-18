import uuid
import md5

def get_uuid(string):
    md5sum = md5.new(string)
    uuid_str = md5sum.hexdigest()
    new_uuid = uuid.UUID(uuid_str)
    return new_uuid
    
if __name__ == "__main__":
    print get_uuid("hello")