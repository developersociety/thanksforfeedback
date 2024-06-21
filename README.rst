=========================
Thanks for the Feedback
=========================

Development setup
=================

It's recommended you use `virtualenvwrapper <https://virtualenvwrapper.readthedocs.io/en/latest/>`_
and `The Developer Society Dev Tools <https://github.com/developersociety/tools>`_.

Presuming you are using those tools, getting started on this project is pretty straightforward:

.. code:: console

    $ dev-clone thanksforfeedback
    $ workon thanksforfeedback
    $ make reset

Generate some credentials in Google Cloud Console, save as credentials.json.
You can now run the development server:

.. code:: console

    $ make serve

To setup a sheet, you can run a script like this:

.. code:: python

    import gspread
    from oauth2client.service_account import ServiceAccountCredentials
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scope)
    client = gspread.authorize(creds)
    sheet = client.create('My Feedback Log')
    sheet.share('me@example.com', perm_type='user', role='writer')

Make sure the name matches the name in views.py.
