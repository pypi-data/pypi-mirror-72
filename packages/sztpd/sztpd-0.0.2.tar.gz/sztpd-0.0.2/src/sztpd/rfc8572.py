# Copyright (c) 2020 Watsen Networks.  All Rights Reserved.

from __future__ import annotations
_p='ietf-sztp-bootstrap-server'
_o='urn:ietf:params:xml:ns:yang:ietf-sztp-bootstrap-server'
_n='Unable to parse "input" JSON document: '
_m='application/*'
_l='*/*'
_k='ssl_object'
_j='Resource does not exist.'
_i='Requested resource does not exist.'
_h=':log-entry'
_g='/devices/device='
_f=':devices/device='
_e='webhooks'
_d='ietf-sztp-bootstrap-server:input'
_c='Parent node does not exist.'
_b='Resource can not be modified.'
_a='webhook'
_Z='RPC "input" node fails YANG validation here: '
_Y=True
_X='callback'
_W='passed-input'
_V=':device'
_U='1'
_T=':tenants/tenant='
_S='x'
_R='reference'
_Q='name'
_P='Accept'
_O='return-code'
_N='error-message'
_M='path'
_L='method'
_K='source-ip'
_J='timestamp'
_I='application/yang-data+xml'
_H='Content-Type'
_G='application/yang-data+json'
_F='0'
_E=':dynamic-callout'
_D='dynamic-callout'
_C='/'
_B='event-details'
_A=None
import json,base64,pprint,aiohttp,yangson,datetime,basicauth,pkg_resources
from .  import yl
from .  import dal
from .  import utils
from aiohttp import web
from pyasn1.type import univ
from .dal import DataAccessLayer
from .rcsvr import RestconfServer
from .handler import RouteHandler
from pyasn1_modules import rfc5652
from passlib.hash import sha256_crypt
from pyasn1.codec.der.encoder import encode as encode_der
from pyasn1.codec.der.decoder import decode as der_decoder
from certvalidator import CertificateValidator,ValidationContext,PathBuildingError
class RFC8572ViewHandler(RouteHandler):
	len_prefix_running=len(RestconfServer.root+'/ds/ietf-datastores:running');len_prefix_operational=len(RestconfServer.root+'/ds/ietf-datastores:operational');len_prefix_operations=len(RestconfServer.root+'/operations');id_ct_sztpConveyedInfoXML=rfc5652._buildOid(1,2,840,113549,1,9,16,1,42);id_ct_sztpConveyedInfoJSON=rfc5652._buildOid(1,2,840,113549,1,9,16,1,43)
	def __init__(A,dal,mode,yl,nvh):A.dal=dal;A.mode=mode;A.nvh=nvh;B=pkg_resources.resource_filename('sztpd','yang/');A.dm=yangson.DataModel(json.dumps(yl),[B])
	async def _insert_bootstrapping_log_entry(A,device_id,bootstrapping_log_entry):
		E='/bootstrapping-log';B=device_id
		if A.mode==_F:C=_C+A.dal.app_ns+':device/bootstrapping-log'
		elif A.mode==_U:C=_C+A.dal.app_ns+_f+B[0]+E
		elif A.mode==_S:C=_C+A.dal.app_ns+_T+B[1]+_g+B[0]+E
		D={};D[A.dal.app_ns+_h]=bootstrapping_log_entry;await A.dal.handle_post_opstate_request(C,D)
	async def _insert_audit_log_entry(A,tenant_name,audit_log_entry):
		B=tenant_name
		if A.mode==_F or A.mode==_U or B==_A:C=_C+A.dal.app_ns+':audit-log'
		elif A.mode==_S:C=_C+A.dal.app_ns+_T+B+'/audit-log'
		D={};D[A.dal.app_ns+_h]=audit_log_entry;await A.dal.handle_post_opstate_request(C,D)
	async def handle_get_opstate_request(E,request):
		C=request;D=C.path[E.len_prefix_operational:];F=await E._check_auth(C,D)
		if F is _A:return web.Response(status=401)
		A={};A[_J]=datetime.datetime.utcnow();A[_K]=C.remote;A[_L]=C.method;A[_M]=C.path
		if D=='/ietf-yang-library:yang-library'or D==_C or D=='':B=web.Response(status=200);B.content_type=_G;B.text=getattr(yl,'sbi_rfc8572')()
		else:B=web.Response(status=400);B.text=_i;A[_N]=B.text
		A[_O]=B.status;await E._insert_bootstrapping_log_entry(F,A);return B
	async def handle_get_config_request(D,request):
		B=request;E=B.path[D.len_prefix_running:];F=await D._check_auth(B,E)
		if F is _A:return web.Response(status=401)
		A={};A[_J]=datetime.datetime.utcnow();A[_K]=B.remote;A[_L]=B.method;A[_M]=B.path
		if E==_C or E=='':C=web.Response(status=204)
		else:C=web.Response(status=400);C.text=_i;A[_N]=C.text
		A[_O]=C.status;await D._insert_bootstrapping_log_entry(F,A);return C
	async def handle_post_config_request(D,request):
		C=request;E=C.path[D.len_prefix_running:];F=await D._check_auth(C,E)
		if F is _A:return web.Response(status=401)
		A={};A[_J]=datetime.datetime.utcnow();A[_K]=C.remote;A[_L]=C.method;A[_M]=C.path
		if E==_C or E=='':B=web.Response(status=400);B.text=_b
		else:B=web.Response(status=404);B.text=_c
		A[_O]=B.status;A[_N]=B.text;await D._insert_bootstrapping_log_entry(F,A);return B
	async def handle_put_config_request(D,request):
		C=request;E=C.path[D.len_prefix_running:];F=await D._check_auth(C,E)
		if F is _A:return web.Response(status=401)
		A={};A[_J]=datetime.datetime.utcnow();A[_K]=C.remote;A[_L]=C.method;A[_M]=C.path
		if E==_C or E=='':B=web.Response(status=400);B.text=_b
		else:B=web.Response(status=404);B.text=_c
		A[_O]=B.status;A[_N]=B.text;await D._insert_bootstrapping_log_entry(F,A);return B
	async def handle_delete_config_request(D,request):
		C=request;E=C.path[D.len_prefix_running:];F=await D._check_auth(C,E)
		if F is _A:return web.Response(status=401)
		A={};A[_J]=datetime.datetime.utcnow();A[_K]=C.remote;A[_L]=C.method;A[_M]=C.path
		if E==_C or E=='':B=web.Response(status=400);B.text=_b
		else:B=web.Response(status=404);B.text=_c
		A[_O]=B.status;A[_N]=B.text;await D._insert_bootstrapping_log_entry(F,A);return B
	async def handle_action_request(D,request):
		C=request;E=C.path[D.len_prefix_operational:];F=await D._check_auth(C,E)
		if F is _A:return web.Response(status=401)
		A={};A[_J]=datetime.datetime.utcnow();A[_K]=C.remote;A[_L]=C.method;A[_M]=C.path
		if E==_C or E=='':B=web.Response(status=400);B.text="Resource doesn't support action."
		else:B=web.Response(status=404);B.text=_j
		A[_O]=B.status;A[_N]=B.text;await D._insert_bootstrapping_log_entry(F,A);return B
	async def handle_rpc_request(D,request):
		C=request;E=C.path[D.len_prefix_operations:];F=await D._check_auth(C,E)
		if F is _A:return web.Response(status=401)
		B={};B[_J]=datetime.datetime.utcnow();B[_K]=C.remote;B[_L]=C.method;B[_M]=C.path
		if E=='/ietf-sztp-bootstrap-server:get-bootstrapping-data':
			try:A=await D._handle_get_bootstrapping_data_rpc(F,C,B)
			except NotImplementedError as G:A=web.Response(status=501);A.text=str(G)
		elif E=='/ietf-sztp-bootstrap-server:report-progress':
			try:A=await D._handle_report_progress_rpc(F,C,B)
			except NotImplementedError as G:A=web.Response(status=501);A.text=str(G)
		elif E==_C or E=='':A=web.Response(status=400);A.text=_j
		else:A=web.Response(status=404);A.text='Unrecognized RPC.'
		B[_O]=A.status
		if not(A.status>=200 and A.status<=299):B[_N]=A.text
		await D._insert_bootstrapping_log_entry(F,B);return A
	async def _check_auth(B,request,data_path):
		o='local-truststore-reference';n=':device-type';m='identity-certificates';l='activation-code';k='" not found for any tenant.';j='Device "';X='verification';W='device-type';I='comment';H='failure';G='outcome';E=request;A={};A[_J]=datetime.datetime.utcnow();A[_K]=E.remote;A['source-proxies']=list(E.forwarded);A['host']=E.host;A[_L]=E.method;A[_M]=E.path;J=set();L=E.transport.get_extra_info('peercert')
		if L is not _A:P=L['subject'][-1][0][1];J.add(P)
		M=_A;Q=_A;N=E.headers.get('AUTHORIZATION')
		if N!=_A:M,Q=basicauth.decode(N);J.add(M)
		if len(J)==0:A[G]=H;A[I]='Device provided no identification credentials.';await B._insert_audit_log_entry(_A,A);return _A
		if len(J)!=1:A[G]=H;A[I]='Device provided mismatched authentication credentials ('+P+' != '+M+').';await B._insert_audit_log_entry(_A,A);return _A
		D=J.pop();C=_A
		if B.mode==_F:K=_C+B.dal.app_ns+_V
		elif B.mode==_U:K=_C+B.dal.app_ns+_f+D
		if B.mode!=_S:
			try:C=await B.dal.handle_get_config_request(K)
			except dal.NodeNotFound as R:A[G]=H;A[I]=j+D+k;await B._insert_audit_log_entry(_A,A);return _A
			F=_A
		else:
			try:F=await B.dal.get_tenant_name_for_global_key(_C+B.dal.app_ns+':tenants/tenant/devices/device',D)
			except dal.NodeNotFound as R:A[G]=H;A[I]=j+D+k;await B._insert_audit_log_entry(_A,A);return _A
			K=_C+B.dal.app_ns+_T+F+_g+D;C=await B.dal.handle_get_config_request(K)
		assert C!=_A;assert B.dal.app_ns+_V in C;C=C[B.dal.app_ns+_V]
		if B.mode!=_F:C=C[0]
		if l in C:
			if N==_A:A[G]=H;A[I]='Activation code required but none passed for serial number '+D;await B._insert_audit_log_entry(F,A);return _A
			S=C[l];assert S.startswith('$5$')
			if not sha256_crypt.verify(Q,S):A[G]=H;A[I]='Activation code mismatch for serial number '+D;await B._insert_audit_log_entry(F,A);return _A
		else:0
		assert W in C;Y=_C+B.dal.app_ns+':device-types/device-type='+C[W];T=await B.dal.handle_get_config_request(Y)
		if m in T[B.dal.app_ns+n][0]:
			if L is _A:A[G]=H;A[I]='Client cert required but none passed for serial number '+D;await B._insert_audit_log_entry(F,A);return _A
			U=E.transport.get_extra_info(_k);assert U is not _A;Z=U.getpeercert(_Y);O=T[B.dal.app_ns+n][0][m];assert X in O;assert o in O[X];V=O[X][o];a=_C+B.dal.app_ns+':truststore/certificate-bags/certificate-bag='+V['certificate-bag']+'/certificate='+V['certificate'];b=await B.dal.handle_get_config_request(a);c=b[B.dal.app_ns+':certificate'][0]['cert'];d=base64.b64decode(c);e,f=der_decoder(d,asn1Spec=rfc5652.ContentInfo());assert not f;g=utils.degenerate_cms_obj_to_ders(e);h=ValidationContext(trust_roots=g);i=CertificateValidator(Z,validation_context=h)
			try:i._validate_path()
			except PathBuildingError as R:A[G]=H;A[I]="Client cert for serial number '"+D+"' doesn't validate using trust anchors specified by device-type '"+C[W]+"'";await B._insert_audit_log_entry(F,A);return _A
		A[G]='success';await B._insert_audit_log_entry(F,A);return[D,F]
	async def _handle_get_bootstrapping_data_rpc(B,device_id,request,bootstrapping_log_entry):
		Am='ietf-sztp-bootstrap-server:output';Al='ASCII';Ak='contentType';Aj=':configuration';Ai='configuration-handling';Ah='script';Ag='hash-value';Af='hash-algorithm';Ae='address';Ad='referenced-definition';Ac='exited-normally';Ab='function';Aa='plugin';AZ='callout-type';AY='serial-number';AX='rpc-supported';AW='not';AV='match-criteria';AU='matched-response';AT='input';AD='post-configuration-script';AC='configuration';AB='pre-configuration-script';AA='os-version';A9='os-name';A8='trust-anchor';A7='port';A6='bootstrap-server';A5='ietf-sztp-conveyed-info:redirect-information';A4='response-manager';v='image-verification';u='download-uri';t='boot-image';s='callback-results';r='selected-response';q='value';k=device_id;j='onboarding-information';f='error-tag';e='key';c='ietf-sztp-conveyed-info:onboarding-information';b='redirect-information';a='error';W='ietf-restconf:errors';K='response';I='managed-response';H='response-details';G=request;E='get-bootstrapping-data-event';D=bootstrapping_log_entry;C='conveyed-information'
		if G.body_exists:
			if not _H in G.headers:A=web.Response(status=400);A.text='Content-Type must be specified when request bodies are passed (auto-sensing not supported).';return A
			if not any((G.headers[_H]==A for A in(_G,_I))):A=web.Response(status=415);A.text='Content-Type, when specified, must be either "application/yang-data+json" or "application/yang-data+xml".';return A
		if _P in G.headers:
			if not any((G.headers[_P]==A for A in(_l,_m,_G,_I))):A=web.Response(status=406);A.text='"Accept, when specified, must be "*/*", "application/*", "application/yang-data+json", or "application/yang-data+xml".';return A
		X=_A
		if G.body_exists:
			if G.headers[_H]==_G:
				try:X=await G.json()
				except json.decoder.JSONDecodeError as Q:A=web.Response(status=400);A.text=_n+str(Q);return A
			else:assert G.headers[_H]==_I;AE=await G.text();AF={_o:_p};X=xmltodict.parse(AE,process_namespaces=_Y,namespaces=AF)
		L=_A
		if X:
			try:L=X[_d]
			except KeyError:A=web.Response(status=400);A.text=_Z+str(Q);return A
			AG=B.dm.get_schema_node('/ietf-sztp-bootstrap-server:get-bootstrapping-data/input')
			try:AG.from_raw(L)
			except yangson.exceptions.RawMemberError as Q:A=web.Response(status=400);A.text=_Z+str(Q);return A
		if B.mode!=_S:N=_C+B.dal.app_ns+':'
		else:N=_C+B.dal.app_ns+_T+k[1]+_C
		if B.mode==_F:w=N+'device'
		else:w=N+'devices/device='+k[0]
		try:P=await B.dal.handle_get_config_request(w)
		except Exception as Q:A=web.Response(status=501);A.text='Unhandled exception: '+str(Q);return A
		assert P!=_A;assert B.dal.app_ns+_V in P;P=P[B.dal.app_ns+_V]
		if B.mode!=_F:P=P[0]
		D[_B]={};D[_B][E]={};D[_B][E][_W]={}
		if X is _A or L is _A:D[_B][E][_W]['no-input-passed']=[_A]
		else:
			D[_B][E][_W][AT]=[]
			for x in L.keys():input={};input[e]=x;input[q]=L[x];D[_B][E][_W][AT].append(input)
		if A4 not in P or AU not in P[A4]:D[_B][E][r]='no-responses-configured';A=web.Response(status=404);A.text='No responses configured.';return A
		F=_A
		for g in P[A4][AU]:
			if not AV in g:F=g;break
			if X is _A:continue
			for O in g[AV]['match']:
				if O[e]not in L:break
				if'present'in O:
					if AW in O:
						if O[e]in L:break
					elif O[e]not in L:break
				elif q in O:
					if AW in O:
						if O[q]==L[O[e]]:break
					elif O[q]!=L[O[e]]:break
				else:raise NotImplementedError("Unrecognized 'match' expression.")
			else:F=g;break
		if F is _A or'none'in F[K]:
			if F is _A:D[_B][E][r]='no-match-found'
			else:D[_B][E][r]=F[_Q]+" (explicit 'none')"
			A=web.Response(status=404);A.text='No matching responses configured.';return A
		D[_B][E][r]=F[_Q];D[_B][E][H]={I:{}}
		if C in F[K]:
			D[_B][E][H][I]={C:{}};M={}
			if _D in F[K][C]:
				D[_B][E][H][I][C]={_D:{}};assert _R in F[K][C][_D];l=F[K][C][_D][_R];D[_B][E][H][I][C][_D][_Q]=l;T=await B.dal.handle_get_config_request(N+'dynamic-callouts/dynamic-callout='+l);assert l==T[B.dal.app_ns+_E][0][_Q];D[_B][E][H][I][C][_D][AX]=T[B.dal.app_ns+_E][0][AX];Y={}
				if B.mode!=_F:Y[AY]=k[0]
				else:Y[AY]='mode-0 == no-sn'
				Y['source-ip-address']=G.remote
				if L:Y['from-device']=L
				y=G.transport.get_extra_info(_k)
				if y:
					z=y.getpeercert(_Y)
					if z:Y['identity-certificate']=z
				if _X in T[B.dal.app_ns+_E][0]:
					D[_B][E][H][I][C][_D][AZ]=_X;A0=T[B.dal.app_ns+_E][0][_X][Aa];A1=T[B.dal.app_ns+_E][0][_X][Ab];D[_B][E][H][I][C][_D]['callback-details']={Aa:A0,Ab:A1};D[_B][E][H][I][C][_D][s]={};J=_A
					try:J=B.nvh.plugins[A0]['functions'][A1](Y)
					except Exception as Q:D[_B][E][H][I][C][_D][s]['exception-thrown']=str(Q);A=web.Response(status=500);A.text='Server encountered an error while trying to generate a response.';return A
					assert J and type(J)==dict
					if W in J:
						assert len(J[W][a])==1
						if any((A==J[W][a][0][f]for A in('invalid-value','too-big','missing-attribute','bad-attribute','unknown-attribute','bad-element','unknown-element','unknown-namespace','malformed-message'))):A=web.Response(status=400)
						elif any((A==J[W][a][0][f]for A in'access-denied')):A=web.Response(status=403)
						elif any((A==J[W][a][0][f]for A in('in-use','lock-denied','resource-denied','data-exists','data-missing'))):A=web.Response(status=409)
						elif any((A==J[W][a][0][f]for A in('rollback-failed','operation-failed','partial-operation'))):A=web.Response(status=500)
						elif any((A==J[W][a][0][f]for A in'operation-not-supported')):A=web.Response(status=501)
						else:raise NotImplementedError('Unrecognized error-tag: '+J[W][a][0][f])
						A.text=json.dumps(J);D[_B][E][H][I][C][_D][s][Ac]='Returning an RPC-error (HTTP code '+str(A.status)+'): '+str(J);return A
					else:D[_B][E][H][I][C][_D][s][Ac]='Returning conveyed information.'
				elif _e in T[B.dal.app_ns+_E][0]:D[_B][E][H][I][C][_D][AZ]=_a;raise NotImplementedError('webhooks callout support pending!')
				else:raise NotImplementedError('unhandled dynamic callout type: '+str(T[B.dal.app_ns+_E][0]))
				M=J
			elif b in F[K][C]:
				D[_B][E][H][I][C]={b:{}};M[A5]={};M[A5][A6]=[]
				if _R in F[K][C][b]:
					d=F[K][C][b][_R];D[_B][E][H][I][C][b]={Ad:d};m=await B.dal.handle_get_config_request(N+'conveyed-information-responses/redirect-information-response='+d)
					for AH in m[B.dal.app_ns+':redirect-information-response'][0][b][A6]:
						U=await B.dal.handle_get_config_request(N+'bootstrap-servers/bootstrap-server='+AH);U=U[B.dal.app_ns+':bootstrap-server'][0];h={};h[Ae]=U[Ae]
						if A7 in U:h[A7]=U[A7]
						if A8 in U:h[A8]=U[A8]
						M[A5][A6].append(h)
				else:raise NotImplementedError('unhandled redirect-information config type: '+str(F[K][C][b]))
			elif j in F[K][C]:
				D[_B][E][H][I][C]={};M[c]={}
				if _R in F[K][C][j]:
					d=F[K][C][j][_R];D[_B][E][H][I][C][j]={Ad:d};m=await B.dal.handle_get_config_request(N+'conveyed-information-responses/onboarding-information-response='+d);R=m[B.dal.app_ns+':onboarding-information-response'][0][j]
					if t in R:
						AI=R[t];AJ=await B.dal.handle_get_config_request(N+'boot-images/boot-image='+AI);S=AJ[B.dal.app_ns+':boot-image'][0];M[c][t]={};Z=M[c][t]
						if A9 in S:Z[A9]=S[A9]
						if AA in S:Z[AA]=S[AA]
						if u in S:
							Z[u]=list()
							for AK in S[u]:Z[u].append(AK)
						if v in S:
							Z[v]=list()
							for A2 in S[v]:n={};n[Af]=A2[Af];n[Ag]=A2[Ag];Z[v].append(n)
					if AB in R:AL=R[AB];AM=await B.dal.handle_get_config_request(N+'scripts/pre-configuration-script='+AL);M[c][AB]=AM[B.dal.app_ns+':pre-configuration-script'][0][Ah]
					if AC in R:AN=R[AC];A3=await B.dal.handle_get_config_request(N+'configurations/configuration='+AN);M[c][Ai]=A3[B.dal.app_ns+Aj][0][Ai];M[c][AC]=A3[B.dal.app_ns+Aj][0]['config']
					if AD in R:AO=R[AD];AP=await B.dal.handle_get_config_request(N+'scripts/post-configuration-script='+AO);M[c][AD]=AP[B.dal.app_ns+':post-configuration-script'][0][Ah]
			else:raise NotImplementedError('unhandled conveyed-information type: '+str(F[K][C]))
		else:raise NotImplementedError('unhandled response type: '+str(F[K]))
		V=_A
		if _P in G.headers:
			if any((G.headers[_P]==A for A in(_G,_I))):V=G.headers[_P]
		if V is _A:V=G.headers[_H]
		if V==_I:raise NotImplementedError('XML-based response not implemented yet...')
		i=rfc5652.ContentInfo()
		if V==_G:i[Ak]=B.id_ct_sztpConveyedInfoJSON;i['content']=encode_der(json.dumps(M,indent=4),asn1Spec=univ.OctetString())
		else:assert V==_I;i[Ak]=B.id_ct_sztpConveyedInfoXML;raise NotImplementedError('XML based responses not supported.')
		AQ=encode_der(i,rfc5652.ContentInfo());o=base64.b64encode(AQ).decode(Al);AR=base64.b64decode(o);AS=base64.b64encode(AR).decode(Al);assert o==AS;p={};p[Am]={};p[Am][C]=o;A=web.Response(status=200);A.content_type=V;A.text=json.dumps(p,indent=4);return A
	async def _handle_report_progress_rpc(B,device_id,request,bootstrapping_log_entry):
		e='remote-port';d='wn-sztpd-rpcs:input';c='webhook-results';T='tcp-client-parameters';S='encoding';Q=device_id;P='http';M='dynamic-callout-result';H='report-progress-event';E=bootstrapping_log_entry;C=request
		if _H not in C.headers:A=web.Response(status=400);A.text='Request missing the "Content-Type" header (RFC 8040, 5.2).';return A
		if not any((C.headers[_H]==A for A in(_G,_I))):A=web.Response(status=415);A.text='Content-Type must be "application/yang-data+json" or "application/yang-data+xml".';return A
		if _P in C.headers:
			if not any((C.headers[_P]==A for A in(_l,_m,_G,_I))):A=web.Response(status=406);A.text='The "Accept" type, when set, must be "*/*", "application/*", "application/yang-data+json", or "application/yang-data+xml".';return A
		G=_A
		if not C.body_exists:A=web.Response(status=400);A.text='Missing "input" document';return A
		if C.headers[_H]==_G:
			try:G=await C.json()
			except json.decoder.JSONDecodeError as F:A=web.Response(status=400);A.text=_n+str(F);return A
		else:assert C.headers[_H]==_I;U=await C.text();V={_o:_p};G=xmltodict.parse(U,process_namespaces=_Y,namespaces=V)
		assert not G is _A
		try:W=G[_d]
		except KeyError:A=web.Response(status=400);A.text=_Z+str(F);return A
		X=B.dm.get_schema_node('/ietf-sztp-bootstrap-server:report-progress/input')
		try:X.from_raw(W)
		except (yangson.exceptions.RawMemberError,yangson.exceptions.RawTypeError)as F:A=web.Response(status=400);A.text=_Z+str(F);return A
		E[_B]={};E[_B][H]={};E[_B][H][_W]=G[_d];E[_B][H][M]={}
		if B.mode==_F or B.mode==_U:I=_C+B.dal.app_ns+':preferences/notification-delivery'
		elif B.mode==_S:I=_C+B.dal.app_ns+_T+Q[1]+'/preferences/notification-delivery'
		try:Y=await B.dal.handle_get_config_request(I)
		except Exception as F:E[_B][H][M]['no-webhooks-configured']=[_A]
		else:
			N=Y[B.dal.app_ns+':notification-delivery'][_D][_R];E[_B][H][M][_Q]=N
			if B.mode==_F or B.mode==_U:I=_C+B.dal.app_ns+':dynamic-callouts/dynamic-callout='+N
			elif B.mode==_S:I=_C+B.dal.app_ns+_T+Q[1]+'/dynamic-callouts/dynamic-callout='+N
			K=await B.dal.handle_get_config_request(I);E[_B][H][M][c]={_a:[]};O={};O[d]={};O[d]['notification']=G;Z=json.dumps(O);a='FIXME: xml output'
			if _X in K[B.dal.app_ns+_E][0]:raise NotImplementedError('callback support not implemented yet')
			elif _e in K[B.dal.app_ns+_E][0]:
				for D in K[B.dal.app_ns+_E][0][_e][_a]:
					J={};J[_Q]=D[_Q]
					if S not in D or D[S]=='json':R=Z
					elif D[S]=='xml':R=a
					if P in D:
						L='http://'+D[P][T]['remote-address']
						if e in D[P][T]:L+=':'+str(D[P][T][e])
						L+='/send-notification';J['uri']=L
						try:
							async with aiohttp.ClientSession()as b:A=await b.post(L,data=R)
						except aiohttp.client_exceptions.ClientConnectorError as F:J['connection-error']=str(F)
						else:
							J['http-status-code']=A.status
							if A.status==200:break
					else:assert'https'in D;raise NotImplementedError("https-based webhook isn't supported yet.")
					E[_B][H][M][c][_a].append(J)
			else:raise NotImplementedError('unrecognized callout type '+str(K[B.dal.app_ns+_E][0]))
		A=web.Response(status=204);return A