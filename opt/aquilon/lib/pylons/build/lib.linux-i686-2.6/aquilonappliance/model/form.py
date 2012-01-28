import formencode

class SimpleRealm(formencode.validators.String):
    def _to_python(self, value, c):
         if not realm_re.match(value):
             FAIL XXX

class RealmForm(formencode.Schema):
    allow_extra_fields = True
    filter_extra_fields = True
    realm = formencode.validators.Email(not_empty=True)

