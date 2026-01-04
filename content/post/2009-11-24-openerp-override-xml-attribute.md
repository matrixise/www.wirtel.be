---
title: OpenERP Introduces XML Attribute Overriding in Views
date: 2009-11-24
slug: openerp-override-xml-attribute
tags:
- openerp
- xml
lang: en
modified: 2026-01-04T17:37:22+01:00

---

# OpenERP - How to override an xml attribute in an xml view

A nice feature has been developed in the trunk version of OpenERP.
It's possible to override an xml attribute of an openerp view with the
'attributes' position.

For Example:

```xml
<?xml version="1.0" encoding="UTF-8" ?>
<openerp>
    <data>
        <record model="ir.ui.view" id="res_partner_form">
            <field name="name">res.partner.form</field>
            <field name="model">res.partner</field>
            <field name="type">form</field>
            <field name="inherit_id" ref="base.view_partner_form" />
            <field name="arch" type="xml">
                <xpath expr="/form/notebook/page[@string='General']/field[@name='address']/tree"
                       position="attributes">
                    <attribute name="editable">top</attribute>
                </xpath>
            </field>
        </record>
    </data>
</openerp>
```

Just an update, If you want to use this feature with a page, don't
forget to remove the last '/' in the xpath expression.

```xml
<record id="base.view_crm_partner_info_History" model="ir.ui.view">
    <field name="name">res.partner.crm.history.inherit1</field>
    <field name="model">res.partner</field>
    <field name="type">form</field>
    <field name="inherit_id" ref="base.view_partner_form"/>
    <field name="arch" type="xml">
        <xpath expr="/form/notebook/page[@string='History']" position="attributes">
            <attribute name="invisible">False</attribute>
        </xpath>
    </field>
</record>
```