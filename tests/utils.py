from datetime import datetime, timedelta
import json
from jsonschema import validate

from flask_restful import Resource, Api
from flask import Flask, Response, request
from flask_sqlalchemy import SQLAlchemy

from inlibris.models import Patron, Book, Hold, Loan
from inlibris.constants import *

'''
This is a collection of random utility functions and classes for the testing suite.
'''

def _populate_db(db):
    '''
    Helper function to populate the database for testing and demonstration. Creates two patrons, three books, two loans and two holds.

    Also called in models.py so don't go deleting too quickly.
    '''

    patron1 = Patron(
        barcode=100001,
        firstname="Hilma",
        lastname="Kirjastontäti",
        email="hilma@kirjasto.fi",
        group="Staff",
        status="Active",
        regdate=datetime(2020,1,1)
    )

    patron2 = Patron(
        barcode=100002,
        firstname="Testi",
        lastname="Käyttäjä",
        email="kayttaja@test.com",
        regdate=datetime(1999,12,31)
    )

    patron3 = Patron(
        barcode=100003,
        firstname="Sally",
        lastname="Stover",
        email="sally@test.com",
        regdate=datetime(1991,7,1)
    )

    patron4 = Patron(
        barcode=100004,
        firstname="Shelby",
        lastname="Sunstar",
        email="shelby@test.com",
        regdate=datetime(1990,12,1)
    )

    patron5 = Patron(
        barcode=100005,
        firstname="Sydney",
        lastname="Springer",
        email="sydney@test.com",
        regdate=datetime(1979,10,11)
    )

    patron6 = Patron(
        barcode=100006,
        firstname="Shirley",
        lastname="Starr",
        email="shirley@test.com",
        regdate=datetime(1993,3,3)
    )

    patron7 = Patron(
        barcode=100027,
        firstname="Sadie",
        lastname="Seymour",
        email="sadie@test.com",
        regdate=datetime(1992,11,11)
    )

    patron8 = Patron(
        barcode=105312,
        firstname="Stacey",
        lastname="Stringer",
        email="stacey@test.com",
        regdate=datetime(2002,4,19)
    )

    patron9 = Patron(
        barcode=101127,
        firstname="Sarah",
        lastname="Slaughter",
        email="sarah@test.com",
        regdate=datetime(2000,1,1)
    )

    patron10 = Patron(
        barcode=102112,
        firstname="Stacy",
        lastname="Snyder",
        email="stacy@test.com",
        regdate=datetime(1999,12,31)
    )

    patron11 = Patron(
        barcode=100011,
        firstname="Samantha",
        lastname="Stocker",
        email="samantha@test.com",
        regdate=datetime(2007,6,1)
    )

    item1 = Book(
        barcode=200001,
        title="Garpin maailma",
        author="Irving, John",
        pubyear=2011,
        format="book",
        description="ISBN 978-951-31-1264-6"
    )

    item2 = Book(
        barcode=200002,
        title="Minä olen monta",
        author="Irving, John",
        pubyear=2013,
        format="book",
        description="ISBN 978-951-31-7092-9"
    )

    item3 = Book(
        barcode=200003,
        title="Oman elämänsä sankari",
        author="Irving, John",
        pubyear=2009,
        format="book",
        description="ISBN 978-951-31-6307-8"
    )

    item4 = Book(
        barcode=200004,
        title="Kaikki isäni hotellit",
        author="Irving, John",
        pubyear=1982,
        format="book",
        description="ISBN 951-30-5443-8"
    )

    item5 = Book(
        barcode=200005,
        title="Vapauttakaa karhut",
        author="Irving, John",
        pubyear=2012,
        format="book",
        description="ISBN 978-951-31-6650-2"
    )

    item6 = Book(
        barcode=200006,
        title="Viimeinen yö Twisted Riverillä",
        author="Irving, John",
        pubyear=2010,
        format="book",
        description="ISBN 978-951-31-5293-2"
    )

    item7 = Book(
        barcode=200007,
        title="Ystäväni Owen Meany",
        author="Irving, John",
        pubyear=1990,
        format="book",
        description="ISBN 951-30-8982-7"
    )

    loan1 = Loan(
        book=item1,
        patron=patron2,
        loandate=datetime(2020,4,20).date(),
        duedate=(datetime(2020,4,20) + timedelta(days=28)).date()
    )

    loan2 = Loan(
        book=item3,
        patron=patron2,
        loandate=datetime(2020,4,17).date(),
        duedate=(datetime(2020,4,17) + timedelta(days=28)).date()
    )

    loan3 = Loan(
        book=item5,
        patron=patron4,
        loandate=datetime(2020,4,11).date(),
        duedate=(datetime(2020,4,11) + timedelta(days=28)).date()
    )

    loan4 = Loan(
        book=item6,
        patron=patron5,
        loandate=datetime(2020,4,2).date(),
        duedate=(datetime(2020,4,2) + timedelta(days=28)).date()
    )

    hold1 = Hold(
        book=item1,
        patron=patron1,
        holddate=datetime(2020,4,2).date(),
        expirationdate=(datetime(2020,4,2) + timedelta(days=45)).date()
    )

    hold2 = Hold(
        book=item3,
        patron=patron1,
        holddate=datetime(2020,4,2).date(),
        expirationdate=(datetime(2020,4,2) + timedelta(days=45)).date()
    )

    db.session.add(patron1)
    db.session.add(patron2)
    db.session.add(patron3)
    db.session.add(patron4)
    db.session.add(patron5)
    db.session.add(patron6)
    db.session.add(patron7)
    db.session.add(patron8)
    db.session.add(patron9)
    db.session.add(patron10)
    db.session.add(patron11)
    db.session.add(item1)
    db.session.add(item2)
    db.session.add(item3)
    db.session.add(item4)
    db.session.add(item5)
    db.session.add(item6)
    db.session.add(item7)
    db.session.add(loan1)
    db.session.add(loan2)
    db.session.add(loan3)
    db.session.add(loan4)
    db.session.add(hold1)
    db.session.add(hold2)
    db.session.commit()

'''
Helper functions for API testing.
'''

def _get_patron_json(barcode=123456, email="test@test.com", firstname="Testi"):
    """
    Creates a valid patron JSON object to be used for PUT and POST tests.
    """
    
    return {"barcode": barcode, "firstname": firstname, "email": email}

def _get_book_json(barcode=234567, pubyear=2020):
    """
    Creates a valid book JSON object to be used for PUT and POST tests.
    """
    
    return {"barcode": barcode, "title": "Testikirja", "pubyear": pubyear}

def _get_add_loan_json(book_barcode=200007):
    """
    Creates a valid loan JSON object to be used for POST tests.
    """
    
    return {"book_barcode": book_barcode}

def _get_edit_loan_json(book_barcode=200001, patron_barcode=100002):
    """
    Creates a valid loan JSON object to be used for PUT tests.
    """
    
    return {
        "patron_barcode": patron_barcode,
        "loandate": "2020-03-03",
        "renewaldate": "2020-03-04",
        "duedate": "2020-04-02",
        "renewed": 1,
        "status": "Renewed",
    }

def _check_namespace(client, response):
    """
    Checks that the "inlibris" namespace is found from the response body, and
    that its "name" attribute is a URL that can be accessed.
    """
    
    ns_href = response["@namespaces"]["inlibris"]["name"]
    resp = client.get(ns_href)
    assert resp.status_code == 200

def _check_control_get_method(ctrl, client, obj):
    """
    Checks a GET type control from a JSON object be it root document or an item
    in a collection. Also checks that the URL of the control can be accessed.
    """
    
    href = obj["@controls"][ctrl]["href"]
    resp = client.get(href)
    assert resp.status_code == 200

def _check_control_delete_method(ctrl, client, obj):
    """
    Checks a DELETE type control from a JSON object be it root document or an
    item in a collection. Checks the contrl's method in addition to its "href".
    Also checks that using the control results in the correct status code of 204.
    """
    
    href = obj["@controls"][ctrl]["href"]
    method = obj["@controls"][ctrl]["method"].lower()
    assert method == "delete"
    resp = client.delete(href)
    assert resp.status_code == 204

def _check_control_put_patron_method(ctrl, client, obj):
    """
    Checks a PUT type control from a JSON object be it root document or an item
    in a collection. In addition to checking the "href" attribute, also checks
    that method, encoding and schema can be found from the control. Also
    validates a valid sensor against the schema of the control to ensure that
    they match. Finally checks that using the control results in the correct
    status code of 204.
    """
    
    ctrl_obj = obj["@controls"][ctrl]
    href = ctrl_obj["href"]
    method = ctrl_obj["method"].lower()
    encoding = ctrl_obj["encoding"].lower()
    schema = ctrl_obj["schema"]
    assert method == "put"
    assert encoding == "json"
    body = _get_patron_json()
    body["barcode"] = obj["barcode"]
    body["firstname"] = obj["firstname"]
    body["email"] = obj["email"]
    validate(body, schema)
    resp = client.put(href, json=body)
    assert resp.status_code == 204

def _check_control_put_book_method(ctrl, client, obj):
    """
    Checks a PUT type control from a JSON object be it root document or an item
    in a collection. In addition to checking the "href" attribute, also checks
    that method, encoding and schema can be found from the control. Also
    validates a valid sensor against the schema of the control to ensure that
    they match. Finally checks that using the control results in the correct
    status code of 204.
    """
    
    ctrl_obj = obj["@controls"][ctrl]
    href = ctrl_obj["href"]
    method = ctrl_obj["method"].lower()
    encoding = ctrl_obj["encoding"].lower()
    schema = ctrl_obj["schema"]
    assert method == "put"
    assert encoding == "json"
    body = _get_book_json()
    body["barcode"] = obj["barcode"]
    validate(body, schema)
    resp = client.put(href, json=body)
    assert resp.status_code == 204

def _check_control_put_loan_method(ctrl, client, obj):
    """
    Checks a PUT type control from a JSON object be it root document or an item
    in a collection. In addition to checking the "href" attribute, also checks
    that method, encoding and schema can be found from the control. Also
    validates a valid sensor against the schema of the control to ensure that
    they match. Finally checks that using the control results in the correct
    status code of 204.
    """
    
    ctrl_obj = obj["@controls"][ctrl]
    href = ctrl_obj["href"]
    method = ctrl_obj["method"].lower()
    encoding = ctrl_obj["encoding"].lower()
    schema = ctrl_obj["schema"]
    assert method == "put"
    assert encoding == "json"
    body = _get_edit_loan_json()
    body["book_barcode"] = obj["book_barcode"]
    body["patron_barcode"] = obj["patron_barcode"]
    validate(body, schema)
    resp = client.put(href, json=body)
    assert resp.status_code == 200

def _check_control_post_patron_method(ctrl, client, obj):
    """
    Checks a POST type control from a JSON object be it root document or an item
    in a collection. In addition to checking the "href" attribute, also checks
    that method, encoding and schema can be found from the control. Also
    validates a valid sensor against the schema of the control to ensure that
    they match. Finally checks that using the control results in the correct
    status code of 201.
    """
    
    ctrl_obj = obj["@controls"][ctrl]
    href = ctrl_obj["href"]
    method = ctrl_obj["method"].lower()
    encoding = ctrl_obj["encoding"].lower()
    schema = ctrl_obj["schema"]
    assert method == "post"
    assert encoding == "json"
    body = _get_patron_json()
    validate(body, schema)
    resp = client.post(href, json=body)
    assert resp.status_code == 201

def _check_control_post_book_method(ctrl, client, obj):
    """
    Checks a POST type control from a JSON object be it root document or an item
    in a collection. In addition to checking the "href" attribute, also checks
    that method, encoding and schema can be found from the control. Also
    validates a valid sensor against the schema of the control to ensure that
    they match. Finally checks that using the control results in the correct
    status code of 201.
    """
    
    ctrl_obj = obj["@controls"][ctrl]
    href = ctrl_obj["href"]
    method = ctrl_obj["method"].lower()
    encoding = ctrl_obj["encoding"].lower()
    schema = ctrl_obj["schema"]
    assert method == "post"
    assert encoding == "json"
    body = _get_book_json()
    validate(body, schema)
    resp = client.post(href, json=body)
    assert resp.status_code == 201

def _check_control_post_loan_method(ctrl, client, obj):
    """
    Checks a POST type control from a JSON object be it root document or an item
    in a collection. In addition to checking the "href" attribute, also checks
    that method, encoding and schema can be found from the control. Also
    validates a valid sensor against the schema of the control to ensure that
    they match. Finally checks that using the control results in the correct
    status code of 201.
    """
    
    ctrl_obj = obj["@controls"][ctrl]
    href = ctrl_obj["href"]
    method = ctrl_obj["method"].lower()
    encoding = ctrl_obj["encoding"].lower()
    schema = ctrl_obj["schema"]
    assert method == "post"
    assert encoding == "json"
    body = _get_add_loan_json()
    validate(body, schema)
    resp = client.post(href, json=body)
    assert resp.status_code == 201

'''
Helper functions for database testing.
'''

def _get_patron(barcode=123456, email="test@test.com", firstname="Testi"):
    """
    Create a valid Patron object.
    """
    return Patron(
        barcode=barcode,
        firstname=firstname,
        email=email,
        regdate=datetime.now().date()
    )

def _get_book(barcode=234567, pubyear=2020):
    """
    Create a valid Book object.
    """
    return Book(
        barcode=barcode,
        title="Testikirja",
        pubyear=pubyear
    )

def _get_loan():
    """
    Create a valid Loan object.
    """
    return Loan(
        loandate=datetime.now().date(),
        duedate=(datetime.now() + timedelta(days=28)).date()
    )

def _get_hold():
    """
    Create a valid hold object.
    """
    return Hold(
        holddate=datetime.now().date(),
        expirationdate=(datetime.now() + timedelta(days=100)).date()
    )