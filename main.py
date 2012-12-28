import webapp2,json
import pickle
from google.appengine.ext import db
from google.appengine.ext.webapp import template

class collection(db.Model):
	filename=db.StringProperty()
	imdata=db.StringListProperty()


class MainPage(webapp2.RequestHandler):
	def get(self):
		fl=[]
		imdata=[]
		for i in collection.all():
			fl.append(i.filename)

		filename=self.request.path[1:]

		self.response.out.write('<font size="5">'+filename+'</font>')

		if filename!="":
			for i in collection.all():
				if json.loads(i.filename)==filename:
					for j in i.imdata:
						imdata.append(pickle.loads(j))
					#self.response.out.write(i.filename)
			self.response.out.write('<script>l='+json.dumps(fl)+';fill=0; totaldata=new Array();imdata='+json.dumps(imdata)+';</script>')
		else:
			self.response.out.write('<script>l='+json.dumps(fl)+';fill=0; totaldata=new Array();imdata='+json.dumps("")+' ;</script>')

		self.response.out.write(template.render("paint2.html",{}));
		



	def post(self):
		filnme=self.request.get('filnm')
		imagedata=self.request.get('imagedata')
		Dict=json.loads(imagedata)
		dbase=collection(parent=db.Key.from_path('filename',filnme))
		dbase.filename=filnme
		for i in Dict:
			dbase.imdata.append(pickle.dumps(i))
		q=db.GqlQuery("SELECT * FROM collection WHERE ANCESTOR IS :c",c=db.Key.from_path('filename',filnme))
		c=0
		for i in q:
			c=c+1
			i.imdata=[]
			for j in Dict:
				i.imdata.append(pickle.dumps(j))
			db.put(i)
		if c==0:
			dbase.put()
		self.redirect("/")

app=webapp2.WSGIApplication([('/.*',MainPage)],debug=True)



