from computaco.organizations.company import Company


class Enterprise(Company):
    subsiduaries: list[Company]
