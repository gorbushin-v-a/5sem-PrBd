from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.schema import Table, MetaData

app = Flask(__name__)
engine = create_engine('mysql+mysqldb://root:password@localhost:3306/production?charset=utf8', encoding='utf-8')
Base = declarative_base()
metadata = MetaData(bind=engine)

customers = Table('организация_заказчик', metadata, autoload=True)
sellers = Table('организация_продавец', metadata, autoload=True)
materials = Table('материал', metadata, autoload=True)
orders = Table('заказ', metadata, autoload=True)

orderToProduct = Table('заказ_конечный_продукт', metadata, autoload=True)
orderToMaterial = Table('заказ_материал', metadata, autoload=True)
product = Table('конечный_продукт', metadata, autoload=True)
equipment = Table('оборудование', metadata, autoload=True)
manufacture = Table('производство', metadata, autoload=True)
manufactureToEquipment = Table('производство_оборудование', metadata, autoload=True)
recipe = Table('рецептура', metadata, autoload=True)
equipmentType = Table('тип_оборудования', metadata, autoload=True)
materialCost = Table('цена_материала', metadata, autoload=True)

from sqlalchemy.orm import sessionmaker

Session = sessionmaker(bind=engine)
Session.configure(bind=engine)
session = Session()

ourCustomersex = "SELECT * FROM организация_заказчик"
ourSellersex = "SELECT * FROM организация_продавец"
ourMaterialsex = "SELECT * FROM материал"
ourOrdersex = "SELECT p.номер_заказа, p.описание_заказа, ps.`наименование_организации_заказчика` FROM заказ p INNER JOIN организация_заказчик ps ON p.id_организации_заказчика = ps.id_организации_заказчика;"

ourOrderToProductex = "SELECT p.номер_заказа, p.описание_заказа, ps.`количество`, pc.id_продукта , pc.наименование_продукта FROM заказ p JOIN заказ_конечный_продукт ps ON p.номер_заказа = ps.номер_заказа JOIN конечный_продукт pc ON ps.id_продукта = pc.id_продукта;"
ourOrderToMaterialex = "SELECT p.номер_заказа, p.описание_заказа, ps.`количество`, pc.id_материала , pc.наименование_материала FROM заказ p JOIN заказ_материал ps ON p.номер_заказа = ps.номер_заказа JOIN материал pc ON ps.id_материала = pc.id_материала;"
ourProductex = "SELECT * FROM конечный_продукт"
ourEquipmentex = "SELECT p.id_оборудования, p.название, ps.`наименование_типа` FROM оборудование p INNER JOIN тип_оборудования ps ON p.id_типа = ps.id_типа;"
ourManufactureex = "SELECT p.id_производства, p.название_производства, ps.`наименование_продукта` FROM производство p INNER JOIN конечный_продукт ps ON p.id_продукта = ps.id_продукта;"
ourManufactureToEquipmentex = "SELECT p.id_производства, p.название_производства, ps.`количество`, pc.id_оборудования , pc.название FROM производство p JOIN производство_оборудование ps ON p.id_производства = ps.id_производства JOIN оборудование pc ON ps.id_оборудования = pc.id_оборудования;"
ourRecipeex = "SELECT p.id_материала, p.наименование_материала, ps.`количество`, pc.id_производства , pc.название_производства FROM материал p JOIN рецептура ps ON p.id_материала = ps.id_материала JOIN производство pc ON ps.id_производства = pc.id_производства;"
ourEquipmentTypeex = "SELECT * FROM тип_оборудования"
ourMaterialCostex = "SELECT p.id_материала, p.наименование_материала, ps.`цена`, pc.id_организации_продавца , pc.наименование_организации_продавца FROM материал p JOIN цена_материала ps ON p.id_материала = ps.id_материала JOIN организация_продавец pc ON ps.id_организации_продавца = pc.id_организации_продавца;"


@app.route('/', methods=['GET'])
def index():
    example1 = session.execute("SELECT id_материала FROM материал WHERE наименование_материала = 'Медная руда';")
    example2 = session.execute(
        "SELECT p.цена, p.id_организации_продавца, ps.наименование_материала FROM цена_материала p INNER JOIN материал ps ON p.id_материала = ps.id_материала;")
    example3 = session.execute(
        "SELECT p.наименование_материала, ps.количество FROM материал p INNER JOIN рецептура ps ON p.id_материала = ps.id_материала WHERE (SELECT id_производства FROM производство WHERE название_производства = 'Сплавление бронзы')= ps.`id_производства`;")
    example4 = session.execute(
        "SELECT p1.наименование_материала 'материал', SUM(p2.количество*p5.количество)-p1.количество 'необходимо дозаказать', p1.количество 'имеется' FROM материал p1 JOIN рецептура p2 ON p1.id_материала = p2.id_материала JOIN производство p3 ON p2.id_производства = p3.id_производства JOIN конечный_продукт p4 ON p3.id_продукта = p4.id_продукта JOIN заказ_конечный_продукт p5 ON p4.id_продукта = p5.id_продукта GROUP BY p1.наименование_материала, p1.количество HAVING (SUM(p2.количество*p5.количество)>p1.количество) ORDER BY 2 DESC, 1, 3 LIMIT 3;")

    ourCustomers = session.execute(ourCustomersex)
    ourSellers = session.execute(ourSellersex)
    ourMaterials = session.execute(ourMaterialsex)

    ourProduct = session.execute(ourProductex)
    ourEquipmentType = session.execute(ourEquipmentTypeex)

    ourOrders = session.execute(ourOrdersex)
    ourOrderToProduct = session.execute(ourOrderToProductex)
    ourOrderToMaterial = session.execute(ourOrderToMaterialex)
    ourEquipment = session.execute(ourEquipmentex)
    ourManufacture = session.execute(ourManufactureex)
    ourManufactureToEquipment = session.execute(ourManufactureToEquipmentex)
    ourRecipe = session.execute(ourRecipeex)
    ourMaterialCost = session.execute(ourMaterialCostex)

    ourCustomersList = session.query(customers).all()

    ourOrdersList = session.query(orders).all()
    ourProductList = session.query(product).all()
    ourMaterialList = session.query(materials).all()
    ourManufactureList = session.query(manufacture).all()
    ourEquipmentList = session.query(equipment).all()
    ourSellersList = session.query(sellers).all()
    ourTypeList = session.query(equipmentType).all()

    return render_template("index.html", exampTable=example4, examTable=example3, exaTable=example2, exTable=example1,
                           typeListTable=ourTypeList, sellersListTable=ourSellersList,
                           equipmentListTable=ourEquipmentList, manufactureListTable=ourManufactureList,
                           materialListTable=ourMaterialList, productListTable=ourProductList,
                           ordersListTable=ourOrdersList, customersTable=ourCustomers, sellersTable=ourSellers,
                           materialsTable=ourMaterials, ordersTable=ourOrders, customersListTable=ourCustomersList,
                           orderToProductTable=ourOrderToProduct, orderToMaterialTable=ourOrderToMaterial,
                           productTable=ourProduct, equipmentTable=ourEquipment, manufactureTable=ourManufacture,
                           manufactureToEquipmentTable=ourManufactureToEquipment, recipeTable=ourRecipe,
                           equipmentTypeTable=ourEquipmentType, materialCostTable=ourMaterialCost)


@app.route('/addCustomer', methods=['POST'])
def addCustomer():
    nameCustomer = request.form['fullname']
    info = request.form['info']
    insert_stmnt = customers.insert().values(наименование_организации_заказчика=nameCustomer,
                                             контактная_информация=info)
    session.execute(insert_stmnt)
    return redirect(url_for('index'))


@app.route('/deleteCustomer', methods=['POST'])
def deleteCustomer():
    try:
        session.execute(f"""DELETE FROM организация_заказчик WHERE id_организации_заказчика = """ + request.form[
            'personCustomer'] + """;""")
    except:
        print("error delete consumer");
    return redirect(url_for('index'))


@app.route('/findCustomer', methods=['POST'])
def findCustomer():
    nameCustomer = request.form['fullname']
    info = request.form['info']
    exec = "SELECT * FROM организация_заказчик"
    if nameCustomer != "" or info != "":
        exec += " WHERE "
        if nameCustomer != "" and info != "":
            exec += "наименование_организации_заказчика = '" + nameCustomer + "' AND контактная_информация = '" + info + "'"
        elif nameCustomer != "":
            exec += "наименование_организации_заказчика = '" + nameCustomer + "'"
        elif info != "":
            exec += "контактная_информация = '" + info + "'"
    global ourCustomersex
    ourCustomersex = exec
    return redirect(url_for('index'))


@app.route('/addSeller', methods=['POST'])
def addSeller():
    nameSeller = request.form['fullname']
    info = request.form['info']
    insert_stmnte = sellers.insert().values(наименование_организации_продавца=nameSeller, контактная_информация=info)
    session.execute(insert_stmnte)
    global ourSellers
    ourSellers = session.query(sellers).all()
    return redirect(url_for('index'))


@app.route('/deleteSeller', methods=['POST'])
def deleteSeller():
    try:
        session.execute(f"""DELETE FROM организация_продавец WHERE id_организации_продавца = """ + request.form[
            'personSeller'] + """;""")
    except:
        print("error delete seller");
    global ourSellers
    ourSellers = session.query(sellers).all()
    return redirect(url_for('index'))


@app.route('/findSeller', methods=['POST'])
def findSeller():
    nameSeller = request.form['fullname']
    info = request.form['info']
    exec = "SELECT * FROM организация_продавец"
    if nameSeller != "" or info != "":
        exec += " WHERE "
        if nameSeller != "" and info != "":
            exec += "наименование_организации_продавца = '" + nameSeller + "' AND контактная_информация = '" + info + "'"
        elif nameSeller != "":
            exec += "наименование_организации_продавца = '" + nameSeller + "'"
        elif info != "":
            exec += "контактная_информация = '" + info + "'"
    global ourSellersex
    ourSellersex = exec
    return redirect(url_for('index'))


@app.route('/addMaterial', methods=['POST'])
def addMaterial():
    nameMaterial = request.form['name']
    count = request.form['count']
    insert_stmnte = materials.insert().values(наименование_материала=nameMaterial, количество=count)
    session.execute(insert_stmnte)
    global ourMaterials
    ourMaterials = session.query(materials).all()
    return redirect(url_for('index'))


@app.route('/deleteMaterial', methods=['POST'])
def deleteMaterial():
    try:
        session.execute(f"""DELETE FROM материал WHERE id_материала = """ + request.form['material'] + """;""")
    except:
        print("error delete material");
    global ourMaterials
    ourMaterials = session.query(materials).all()
    return redirect(url_for('index'))


@app.route('/findMaterial', methods=['POST'])
def findMaterial():
    nameMaterial = request.form['fullname']
    info = request.form['info']
    exec = "SELECT * FROM материал"
    if nameMaterial != "" or info != "":
        exec += " WHERE "
        if nameMaterial != "" and info != "":
            exec += "наименование_материала = '" + nameMaterial + "' AND количество = '" + info + "'"
        elif nameMaterial != "":
            exec += "наименование_материала = '" + nameMaterial + "'"
        elif info != "":
            exec += "количество = '" + info + "'"
    global ourMaterialsex
    ourMaterialsex = exec
    return redirect(url_for('index'))


@app.route('/addOrder', methods=['POST'])
def addOrder():
    nameOrder = request.form['name']
    nameCustomer = request.form['nameCustomer']
    insert_stmnte = orders.insert().values(описание_заказа=nameOrder, id_организации_заказчика=nameCustomer)
    session.execute(insert_stmnte)
    return redirect(url_for('index'))


@app.route('/deleteOrder', methods=['POST'])
def deleteOrder():
    try:
        session.execute(f"""DELETE FROM заказ WHERE номер_заказа = """ + request.form['order'] + """;""")
    except:
        print("error delete order");
    return redirect(url_for('index'))


@app.route('/addOrderToProduct', methods=['POST'])
def addOrderToProduct():
    nameOrder = request.form['order']
    nameCount = request.form['countP']
    nameProduct = request.form['product']
    insert_stmnte = orderToProduct.insert().values(номер_заказа=nameOrder, id_продукта=nameProduct,
                                                   количество=nameCount)
    try:
        session.execute(insert_stmnte)
    except:
        print("error add ordersToProduct");
    return redirect(url_for('index'))


@app.route('/deleteOrderToProduct', methods=['POST'])
def deleteOrderToProduct():
    try:
        session.execute(f"""DELETE FROM заказ_конечный_продукт WHERE номер_заказа = """ + request.form[
            'value1'] + """ AND id_продукта = """ + request.form['value2'] + """;""")
    except:
        print("error delete ordersToProduct");
    return redirect(url_for('index'))


@app.route('/addOrderToMaterial', methods=['POST'])
def addOrderToMaterial():
    nameOrder = request.form['order']
    nameCount = request.form['countP']
    nameProduct = request.form['product']
    insert_stmnte = orderToMaterial.insert().values(номер_заказа=nameOrder, id_материала=nameProduct,
                                                    количество=nameCount)
    try:
        session.execute(insert_stmnte)
    except:
        print("error add orderToMaterial");
    return redirect(url_for('index'))


@app.route('/deleteOrderToMaterial', methods=['POST'])
def deleteOrderToMaterial():
    try:
        session.execute(f"""DELETE FROM заказ_материал WHERE номер_заказа = """ + request.form[
            'value1'] + """ AND id_материала = """ + request.form['value2'] + """;""")
    except:
        print("error delete orderToMaterial");
    return redirect(url_for('index'))


@app.route('/addManufactureToEquipment', methods=['POST'])
def addManufactureToEquipment():
    nameOrder = request.form['order']
    nameCount = request.form['countP']
    nameProduct = request.form['product']
    insert_stmnte = manufactureToEquipment.insert().values(id_производства=nameOrder, id_оборудования=nameProduct,
                                                           количество=nameCount)
    try:
        session.execute(insert_stmnte)
    except:
        print("error add orderToMaterial");
    return redirect(url_for('index'))


@app.route('/deleteManufactureToEquipment', methods=['POST'])
def deleteManufactureToEquipment():
    try:
        session.execute(f"""DELETE FROM производство_оборудование WHERE id_производства = """ + request.form[
            'value1'] + """ AND id_оборудования = """ + request.form['value2'] + """;""")
    except:
        print("error delete orderToMaterial");
    return redirect(url_for('index'))


@app.route('/addRecipe', methods=['POST'])
def addRecipe():
    nameOrder = request.form['product']
    nameCount = request.form['countP']
    nameProduct = request.form['order']
    insert_stmnte = manufactureToEquipment.insert().values(id_материала=nameOrder, id_производства=nameProduct,
                                                           количество=nameCount)
    try:
        session.execute(insert_stmnte)
    except:
        print("error add recipe");
    return redirect(url_for('index'))


@app.route('/deleteRecipe', methods=['POST'])
def deleteRecipe():
    try:
        session.execute(f"""DELETE FROM производство_оборудование WHERE id_материала = """ + request.form[
            'value1'] + """ AND id_производства = """ + request.form['value2'] + """;""")
    except:
        print("error delete recipe");
    return redirect(url_for('index'))


@app.route('/addCost', methods=['POST'])
def addCost():
    nameOrder = request.form['product']
    nameCount = request.form['countP']
    nameProduct = request.form['order']
    insert_stmnte = manufactureToEquipment.insert().values(id_материала=nameOrder, цена=nameCount,
                                                           id_организации_продавца=nameProduct)
    try:
        session.execute(insert_stmnte)
    except:
        print("error add");
    return redirect(url_for('index'))


@app.route('/deleteCost', methods=['POST'])
def deleteCost():
    try:
        session.execute(f"""DELETE FROM производство_оборудование WHERE id_материала = """ + request.form[
            'value1'] + """ AND id_организации_продавца = """ + request.form['value2'] + """;""")
    except:
        print("error delete");
    return redirect(url_for('index'))


@app.route('/addProduct', methods=['POST'])
def addProduct():
    nameOrder = request.form['product']
    insert_stmnte = product.insert().values(наименование_продукта=nameOrder)
    try:
        session.execute(insert_stmnte)
    except:
        print("error add");
    return redirect(url_for('index'))


@app.route('/deleteProduct', methods=['POST'])
def deleteProduct():
    try:
        session.execute(f"""DELETE FROM конечный_продукт WHERE id_продукта = """ + request.form['order'] + """;""")
    except:
        print("error delete");
    return redirect(url_for('index'))


@app.route('/addType', methods=['POST'])
def addType():
    nameOrder = request.form['type']
    insert_stmnte = equipmentType.insert().values(наименование_типа=nameOrder)
    try:
        session.execute(insert_stmnte)
    except:
        print("error add");
    return redirect(url_for('index'))


@app.route('/deleteType', methods=['POST'])
def deleteType():
    try:
        session.execute(f"""DELETE FROM тип_оборудования WHERE id_типа = """ + request.form['order'] + """;""")
    except:
        print("error delete");
    return redirect(url_for('index'))


@app.route('/addEq', methods=['POST'])
def addEq():
    nameOrder = request.form['name']
    nameType = request.form['type']
    insert_stmnte = equipment.insert().values(название=nameOrder, id_типа=nameType)
    try:
        session.execute(insert_stmnte)
    except:
        print("error add");
    return redirect(url_for('index'))


@app.route('/deleteEq', methods=['POST'])
def deleteEq():
    try:
        session.execute(f"""DELETE FROM оборудование WHERE id_оборудования = """ + request.form['order'] + """;""")
    except:
        print("error delete");
    return redirect(url_for('index'))


@app.route('/addMf', methods=['POST'])
def addMf():
    nameProduct = request.form['type']
    name = request.form['name']
    insert_stmnte = manufacture.insert().values(id_продукта=nameProduct, название_производства=name)
    try:
        session.execute(insert_stmnte)
    except:
        print("error add");
    return redirect(url_for('index'))


@app.route('/deleteMf', methods=['POST'])
def deleteMf():
    try:
        session.execute(f"""DELETE FROM производство WHERE id_производства = """ + request.form['order'] + """;""")
    except:
        print("error delete");
    return redirect(url_for('index'))


@app.route('/roll', methods=['POST'])
def roll():
    session.rollback()
    return redirect(url_for('index'))


@app.route('/commit', methods=['POST'])
def commit():
    session.commit()
    return redirect(url_for('index'))


if __name__ == '__main__':
    import os

    HOST = os.environ.get('SERVER_HOST', 'localhost')
    try:
        PORT = int(os.environ.get('SERVER_PORT', '5555'))
    except ValueError:
        PORT = 5555
    app.run(HOST, PORT)
